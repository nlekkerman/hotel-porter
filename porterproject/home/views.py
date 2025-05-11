import qrcode
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from io import BytesIO
from room.models import Room

def generate_qr(request, room_number):
    url = f"http://127.0.0.1:8000/room/{room_number}/order/"
    qr = qrcode.make(url)

    # Save QR code to memory
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

    return render(request, 'home/show_qr.html', {
        'room_number': room_number,
        'qr_code_base64': img_str
    })

def home(request):
    return render(request, 'home/index.html')

