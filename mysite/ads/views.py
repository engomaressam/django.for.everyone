from django.views.generic import ListView, DetailView
from django.urls import reverse_lazy
from .models import Ad
from .owner import OwnerCreateView, OwnerUpdateView, OwnerDeleteView

class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'

class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'

class AdCreateView(OwnerCreateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = 'ads/ad_form.html'

class AdUpdateView(OwnerUpdateView):
    model = Ad
    fields = ['title', 'price', 'text']
    template_name = 'ads/ad_form.html'

class AdDeleteView(OwnerDeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'