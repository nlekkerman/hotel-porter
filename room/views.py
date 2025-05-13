from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomServiceItem, Order, OrderItem,BreakfastItem
from django.http import JsonResponse
from guest.models import Guest
from django.views.decorators.csrf import csrf_exempt
from .forms import GuestForm
from django.core.paginator import Paginator

 
def add_guest(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = GuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.room = room
            guest.save()
            room.is_occupied = True
            room.save()
            return redirect('room:room_list')  # Or wherever you want
    else:
        form = GuestForm()
    return render(request, 'room/add_guest.html', {'form': form, 'room': room})

def room_list(request):
    rooms = Room.objects.all()  # Get all rooms
    paginator = Paginator(rooms, 10)  # Show 10 rooms per page
    
    page_number = request.GET.get('page')  # Get the page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the page object
    
    return render(request, 'room/room_list.html', {'page_obj': page_obj})


@csrf_exempt
def add_to_order(request, room_number):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = RoomServiceItem.objects.get(id=item_id)

        # Get or create the current order for the room
        order, created = Order.objects.get_or_create(room_number=room_number, status='pending')

        # Get or create the order item
        order_item, created = OrderItem.objects.get_or_create(order=order, item=item)
        if not created:
            order_item.quantity += 1
            order_item.save()

        return JsonResponse({
            'success': True,
            'item_name': item.name,
            'quantity': order_item.quantity,
            'added_at': order_item.order.created_at.strftime('%Y-%m-%d %H:%M'),
        })

    return JsonResponse({'success': False}, status=400)


def view_order(request, room_number):
    SERVICE_CHARGE = 5  # fixed service charge

    try:
        order = Order.objects.filter(room_number=room_number, status='pending').latest('created_at')
    except Order.DoesNotExist:
        order = None

    order_items = []
    subtotal = 0

    if order:
        items = OrderItem.objects.filter(order=order).select_related('item')
        for order_item in items:
            item_total = order_item.item.price * order_item.quantity
            subtotal += item_total
            order_items.append({
                'item': order_item.item,
                'quantity': order_item.quantity,
                'item_total': item_total
            })

    total_price = subtotal + SERVICE_CHARGE

    return render(request, 'room/view_order.html', {
        'room_number': room_number,
        'order_items': order_items,
        'subtotal': subtotal,
        'service_charge': SERVICE_CHARGE,
        'total_price': total_price
    })


def kids_entertainment_view(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    return render(request, 'room/kids_entertainment.html', {'room': room})


def room_service_menu(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    categorized_menu = RoomServiceItem.objects.values('category').distinct()  # Fetch distinct categories
    menu_items = {}

    if request.method == 'POST':
        pin = request.POST.get('pin')
        
        if pin == room.guest_id_pin:
            # PIN is correct
            for category in categorized_menu:
                category_name = category['category']
                items_in_category = RoomServiceItem.objects.filter(category=category_name)
                menu_items[category_name] = items_in_category
            
            return render(request, 'room/room_service_menu.html', {
                    'room_number': room_number,
                    'menu_items': menu_items
                }) 
        else:
            # Incorrect PIN
            return render(request, 'home/enter_pin.html', {
                'room_number': room_number,
                'error': 'Invalid PIN. Please try again.'
            })

    return render(request, 'home/enter_pin.html', {'room_number': room_number})


def breakfast_menu(request, room_number):
    room = get_object_or_404(Room, room_number=room_number)
    breakfast_items = BreakfastItem.objects.all()  # Load all items if PIN is valid

    if request.method == 'POST':
        pin = request.POST.get('pin')

        if pin == room.guest_id_pin:
            return render(request, 'room/in_room_breakfast.html', {
                'room': room,
                'breakfast_items': breakfast_items
            })
        else:
            return render(request, 'home/enter_pin.html', {
                'room_number': room_number,
                'error': 'Invalid PIN. Please try again.'
            })

    return render(request, 'home/enter_pin.html', {'room_number': room_number})

