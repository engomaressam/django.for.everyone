from django.views.generic import ListView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .models import Ad, Comment
from .owner import OwnerDeleteView
from .forms import CreateForm, CommentForm

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

class AdCreateView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/ad_form.html'

    def get(self, request, *args, **kwargs):
        form = CreateForm()
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, *args, **kwargs):
        form = CreateForm(request.POST, request.FILES or None)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        ad = form.save(commit=False)
        ad.owner = request.user
        f = request.FILES.get('file') or request.FILES.get('picture')
        if f is not None:
            ad.content_type = f.content_type
            ad.picture = f.read()
        ad.save()
        return redirect('ads:all')

class AdUpdateView(LoginRequiredMixin, DetailView):
    model = Ad
    template_name = 'ads/ad_form.html'

    def get(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        form = CreateForm(instance=ad)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        form = CreateForm(request.POST, request.FILES or None, instance=ad)
        if not form.is_valid():
            return render(request, self.template_name, {'form': form})
        ad = form.save(commit=False)
        f = request.FILES.get('file') or request.FILES.get('picture')
        if f is not None:
            ad.content_type = f.content_type
            ad.picture = f.read()
        ad.save()
        return redirect('ads:all')

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'

# Stream picture
class PictureResponse(HttpResponse):
    pass

def stream_file(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if not ad.picture:
        return HttpResponse(status=404)
    response = HttpResponse(ad.picture, content_type=ad.content_type)
    response['Content-Length'] = len(ad.picture)
    return response

# Comment views
class CommentCreateView(LoginRequiredMixin, DetailView):
    def post(self, request, pk):
        ad = get_object_or_404(Ad, pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.owner = request.user
            comment.ad = ad
            comment.save()
        return redirect('ads:ad_detail', pk=pk)

class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'ads/comment_delete.html'
    success_url = reverse_lazy('ads:all')

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)