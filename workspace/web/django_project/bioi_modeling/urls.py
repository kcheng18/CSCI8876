from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='bioi_modeling-home'),
    path('about/', views.about, name='bioi_modeling-about'),
    path('topmodeling/', views.topmodeling, name='bioi_modeling-topmodeling'),
]
