from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_guest, name='add_guest'),
    path('guests/<int:guest_id>/booking/', views.guest_booking, name='guest_booking'),
]
