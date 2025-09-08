from django.urls import path
from . import views

app_name = 'autos'
urlpatterns = [
    path('', views.index, name='index'),
    path('auto/<int:pk>/update/', views.AutoUpdateView.as_view(), name='auto_update'),
]


