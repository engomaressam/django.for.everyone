from django.views.generic import ListView, DetailView, DeleteView, View
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from .models import Ad, Comment, Fav
from .owner import OwnerDeleteView
from .forms import CreateForm, CommentForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.order_by('-updated_at', '-created_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            rows = Fav.objects.filter(user=self.request.user).values('ad_id')
            ctx['favorites'] = [row['ad_id'] for row in rows]
        else:
            ctx['favorites'] = []
        return ctx

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception:
            return redirect('ads:all')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

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

class AdFavoriteBaseView(LoginRequiredMixin, View):
    def post(self, request, pk=None):
        ad = get_object_or_404(Ad, id=pk)
        return ad

@method_decorator(csrf_exempt, name='dispatch')
class AddFavoriteView(AdFavoriteBaseView):
    def post(self, request, pk=None):
        ad = super().post(request, pk)
        Fav.objects.get_or_create(user=request.user, ad=ad)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('ads:all')

@method_decorator(csrf_exempt, name='dispatch')
class DeleteFavoriteView(AdFavoriteBaseView):
    def post(self, request, pk=None):
        ad = super().post(request, pk)
        Fav.objects.filter(user=request.user, ad=ad).delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        return redirect('ads:all')