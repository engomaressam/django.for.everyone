from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Breed, Cat

class CatList(LoginRequiredMixin, ListView):
    model = Cat
    template_name = "cats/cat_list.html"
    context_object_name = "cat_list"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breed_count"] = Breed.objects.count()
        return ctx

class CatCreate(LoginRequiredMixin, CreateView):
    model = Cat
    fields = ["nickname","weight","foods","breed"]
    success_url = reverse_lazy("cats:all")

class CatUpdate(LoginRequiredMixin, UpdateView):
    model = Cat
    fields = ["nickname","weight","foods","breed"]
    success_url = reverse_lazy("cats:all")

class CatDelete(LoginRequiredMixin, DeleteView):
    model = Cat
    success_url = reverse_lazy("cats:all")

class BreedList(LoginRequiredMixin, ListView):
    model = Breed
    template_name = "cats/breed_list.html"

class BreedCreate(LoginRequiredMixin, CreateView):
    model = Breed
    fields = ["name"]
    success_url = reverse_lazy("cats:all")

class BreedUpdate(LoginRequiredMixin, UpdateView):
    model = Breed
    fields = ["name"]
    success_url = reverse_lazy("cats:all")

class BreedDelete(LoginRequiredMixin, DeleteView):
    model = Breed
    success_url = reverse_lazy("cats:all")
