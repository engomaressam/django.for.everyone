from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import UpdateView
from .models import Make, Auto


@login_required(login_url='/accounts/login/')
def index(request: HttpRequest) -> HttpResponse:
    makes = Make.objects.all().count()
    autos = Auto.objects.filter(owner=request.user)
    return render(request, 'autos/index.html', {
        'makes_count': makes,
        'autos': autos,
    })

class AutoUpdateView(UpdateView):
    model = Auto
    fields = ['nickname', 'mileage', 'comments', 'make']
    template_name = 'autos/auto_form.html'
    success_url = '/autos/'
    
    def get_queryset(self):
        return Auto.objects.filter(owner=self.request.user)

# Create your views here.
