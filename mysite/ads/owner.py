from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class OwnerCreateView(LoginRequiredMixin, CreateView):
    """
    Sub-class of CreateView to automatically pass the Request to the Form
    and add the owner to the saved object
    """
    def form_valid(self, form):
        print('form_valid called')
        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

class OwnerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Sub-class of UpdateView to restrict a User to only modify their own data
    """
    def get_queryset(self):
        print('update get_queryset called')
        qs = super(OwnerUpdateView, self).get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerDeleteView(LoginRequiredMixin, DeleteView):
    """
    Sub-class of DeleteView to restrict a User to only modify their own data
    """
    def get_queryset(self):
        print('delete get_queryset called')
        qs = super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)
