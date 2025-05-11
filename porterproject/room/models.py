from django.db import models
import cloudinary
import cloudinary.uploader
import qrcode
from io import BytesIO


class Room(models.Model):
    room_number = models.IntegerField(unique=True)
    guest_id_pin = models.CharField(max_length=4, unique=True, null=True, blank=True)
    guests = models.ManyToManyField('guest.Guest', related_name='rooms', blank=True)
    is_occupied = models.BooleanField(default=False)

    room_service_qr_code = models.URLField(blank=True, null=True)
    kids_entertainment_qr_code = models.URLField(blank=True, null=True)
    in_room_breakfast_qr_code = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Room {self.room_number}"

    def generate_qr_code(self, qr_type="room_service"):
        path_map = {
            "room_service": f"http://127.0.0.1:8000/room/{self.room_number}/menu/",
            "kids_entertainment": f"http://127.0.0.1:8000/room/{self.room_number}/kids/",
            "in_room_breakfast": f"http://127.0.0.1:8000/room/{self.room_number}/breakfast/",
        }

        qr_field_map = {
            "room_service": "room_service_qr_code",
            "kids_entertainment": "kids_entertainment_qr_code",
            "in_room_breakfast": "in_room_breakfast_qr_code",
        }

        url = path_map.get(qr_type)
        if not url:
            return  # invalid type

        # Generate QR
        qr = qrcode.make(url)
        img_io = BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)

        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(img_io, resource_type="image")
        qr_url = upload_result['secure_url']

        # Save the result in the corresponding field
        setattr(self, qr_field_map[qr_type], qr_url)
        self.save()

class RoomServiceItem(models.Model):
    CATEGORY_CHOICES = [
        ('Starters', 'Starters'),
        ('Mains', 'Mains'),
        ('Desserts', 'Desserts'),
        ('Drinks', 'Drinks'),
        ('Others', 'Others'),
    ]

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='room_service_items/', null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Others')  # ✅ New field

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            upload_result = cloudinary.uploader.upload(self.image)
            self.image = upload_result.get('secure_url', self.image.url)
        super(RoomServiceItem, self).save(*args, **kwargs)
        

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    
    room_number = models.IntegerField()
    items = models.ManyToManyField(RoomServiceItem, through='OrderItem')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Order {self.id} for Room {self.room_number} - Status: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(RoomServiceItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return f"{self.quantity} x {self.item.name} for Order {self.order.id}"
    

class BreakfastItem(models.Model):
    CATEGORY_CHOICES = [
        ('Mains', 'Mains'),
        ('Breads', 'Breads'),
        ('Drinks', 'Drinks'),
        ('Sides', 'Sides'),
    ]

    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='breakfast_items/', null=True, blank=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Mains')
    quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            upload_result = cloudinary.uploader.upload(self.image)
            self.image = upload_result.get('secure_url', self.image.url)
        super().save(*args, **kwargs)


class BreakfastOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    room_number = models.IntegerField()
    items = models.ManyToManyField(BreakfastItem, through='BreakfastOrderItem')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Breakfast Order {self.id} for Room {self.room_number} - {self.status}"


class BreakfastOrderItem(models.Model):
    order = models.ForeignKey(BreakfastOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(BreakfastItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.name} in Breakfast Order {self.order.id}"
