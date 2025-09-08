from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Make, Auto


@login_required(login_url='/accounts/login/')
def index(request: HttpRequest) -> HttpResponse:
    makes = Make.objects.all().count()
    autos = Auto.objects.filter(owner=request.user)
    return render(request, 'autos/index.html', {
        'makes_count': makes,
        'autos': autos,
    })

# Create your views here.
