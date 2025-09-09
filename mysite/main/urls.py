from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout_get/', views.logout_get, name='logout_get'),
]


