from django.shortcuts import render, redirect
from .models import Guest
from room.models import Room   # Assuming you have a Room model in rooms app
def index(request):
    guests = Guest.objects.all()
    return render(request, 'guest/index.html', {'guests': guests})

def add_guest(request):
    if request.method == "POST":
        name = request.POST['name']
        message = request.POST['message']
        Guest.objects.create(name=name, message=message)
        return redirect('index')
    return render(request, 'guest/add_guest.html')

def guest_list(request):
    guests = Guest.objects.all()
    return render(request, 'guests/guest_list.html', {'guests': guests})

def guest_booking(request, guest_id):
    guest = Guest.objects.get(id=guest_id)
    rooms = Room.objects.all()
    
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.get(id=room_id)
        days_booked = request.POST.get('days_booked')
        
        # Update the guest's room and days booked
        guest.room = room
        guest.days_booked = days_booked
        guest.save()
        
        return redirect('guest_list')
    
    return render(request, 'guests/guest_booking.html', {'guest': guest, 'rooms': rooms})


