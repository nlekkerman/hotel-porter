from django.urls import path
from . import views

app_name = 'room'
urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path("rooms/<int:room_id>/add-guest/", views.add_guest, name="add_guest"),
    path('<int:room_number>/add-to-order/', views.add_to_order, name='add_to_order'),
    path('<int:room_number>/order/', views.view_order, name='view_order'),
    path('room/<int:room_number>/menu/', views.room_service_menu, name='room_service_menu'),
    path('room/<int:room_number>/kids/', views.kids_entertainment_view, name='kids_entertainment'),
 path('room/<int:room_number>/breakfast/', views.breakfast_menu, name='breakfast_menu'),]
