import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "porterproject.settings")
django.setup()

# Import the necessary models
from room.models import RoomServiceItem

def create_room_service_items():
    categorized_items = {
        'Starters': [
            {'name': 'Irish Vegetable Soup', 'price': 5.50, 'description': 'A hearty soup with a variety of fresh vegetables.'},
            {'name': 'Smoked Salmon Salad', 'price': 7.50, 'description': 'A light salad with smoked Irish salmon, mixed greens, and a citrus dressing.'},
            {'name': 'Chicken Wings', 'price': 6.00, 'description': 'Crispy chicken wings served with a spicy dip.'},
            {'name': 'Prawn Cocktail', 'price': 8.00, 'description': 'Succulent prawns served with a tangy cocktail sauce.'},
            {'name': 'Bruschetta', 'price': 5.00, 'description': 'Toasted bread topped with tomatoes, garlic, and basil.'},
            {'name': 'Fried Calamari', 'price': 7.00, 'description': 'Crispy fried calamari served with aioli.'},
            {'name': 'Stuffed Mushrooms', 'price': 6.50, 'description': 'Mushrooms stuffed with garlic, cheese, and herbs.'},
            {'name': 'Cheese Plate', 'price': 9.00, 'description': 'An assortment of fine Irish cheeses served with crackers.'},
            {'name': 'Potato Cakes', 'price': 5.50, 'description': 'Crispy potato cakes served with sour cream and chives.'},
        ],
        'Mains': [
            {'name': 'Full Irish Breakfast', 'price': 12.00, 'description': 'Classic Irish breakfast with bacon, eggs, sausages, beans, and toast.'},
            {'name': 'Steak Sandwich', 'price': 15.00, 'description': 'Grilled steak served on toasted bread with a side of chips.'},
            {'name': 'Chicken Curry', 'price': 13.50, 'description': 'Tender chicken in a rich and spicy curry sauce served with rice.'},
            {'name': 'Lamb Stew', 'price': 14.00, 'description': 'Tender lamb cooked in a hearty stew with root vegetables and a rich broth.'},
            {'name': 'Beef and Guinness Pie', 'price': 13.00, 'description': 'A hearty beef pie cooked with Guinness beer and served with mashed potatoes.'},
            {'name': 'Chicken and Mushroom Pie', 'price': 12.50, 'description': 'Creamy chicken and mushrooms encased in flaky pastry.'},
            {'name': 'Vegetarian Lasagna', 'price': 11.00, 'description': 'Layers of pasta, vegetables, and cheese, baked to perfection.'},
            {'name': 'Fish and Chips', 'price': 12.00, 'description': 'Classic battered fish served with crispy chips and tartar sauce.'},
            {'name': 'Pasta Primavera', 'price': 11.50, 'description': 'Pasta with fresh vegetables in a light garlic and olive oil sauce.'},
        ],
        'Desserts': [
            {'name': 'Chocolate Cake', 'price': 6.00, 'description': 'A rich and moist chocolate cake topped with cream.'},
            {'name': 'Apple Tart', 'price': 5.00, 'description': 'Homemade apple tart served with whipped cream.'},
            {'name': 'Banoffee Pie', 'price': 5.50, 'description': 'A delicious dessert made with bananas, toffee, and cream.'},
            {'name': 'Lemon Cheesecake', 'price': 6.50, 'description': 'A tangy lemon cheesecake with a buttery biscuit base.'},
            {'name': 'Sticky Toffee Pudding', 'price': 6.00, 'description': 'A warm sponge cake with toffee sauce, served with vanilla ice cream.'},
            {'name': 'Crème Brûlée', 'price': 7.00, 'description': 'A rich custard dessert with a caramelized sugar topping.'},
            {'name': 'Raspberry Sorbet', 'price': 5.50, 'description': 'A refreshing raspberry sorbet to cleanse your palate.'},
        ],
        'Drinks': [
            {'name': 'Cappuccino', 'price': 3.50, 'description': 'A rich and creamy cappuccino with a perfect foam.'},
            {'name': 'Irish Coffee', 'price': 7.00, 'description': 'A warm Irish coffee made with whiskey, coffee, sugar, and cream.'},
            {'name': 'Guinness Beer', 'price': 5.00, 'description': 'A pint of the famous Irish stout, rich and smooth.'},
            {'name': 'Mineral Water', 'price': 2.00, 'description': 'Refreshing still or sparkling water.'},
            {'name': 'Coca-Cola', 'price': 2.50, 'description': 'Classic Coca-Cola served chilled.'},
            {'name': 'Orange Juice', 'price': 3.00, 'description': 'Freshly squeezed orange juice.'},
            {'name': 'Hot Chocolate', 'price': 3.50, 'description': 'Rich and creamy hot chocolate with whipped cream.'},
            {'name': 'Sparkling Wine', 'price': 8.00, 'description': 'A glass of refreshing sparkling wine.'},
        ],
    }

    for category, items in categorized_items.items():
        for item in items:
            room_service_item = RoomServiceItem(
                name=item['name'],
                category=category,
                price=item['price'],
                description=item['description'],
                image=''  # Still left blank
            )
            room_service_item.save()
            print(f"Created: {item['name']} ({category})")

if __name__ == "__main__":
    create_room_service_items()
    print("All items created with categories.")
