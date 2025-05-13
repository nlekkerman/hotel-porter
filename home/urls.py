from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('generate_qr/<int:room_number>/', views.generate_qr, name='generate_qr'),
]
