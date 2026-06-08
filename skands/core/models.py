import uuid
from decimal import Decimal
from django.db import models


# 24 gouvernorats tunisiens (français - translittération)
GOVERNORATES = (
    ('Ariana', 'Ariana - Aryanah'),
    ('Beja', 'Béja - Baja'),
    ('Ben_Arous', 'Ben Arous - Bin Arus'),
    ('Bizerte', 'Bizerte - Bizerta'),
    ('Gabes', 'Gabès - Qabis'),
    ('Gafsa', 'Gafsa - Qafsa'),
    ('Jendouba', 'Jendouba - Jandouba'),
    ('Kairouan', 'Kairouan - al-Qayrawan'),
    ('Kasserine', 'Kasserine - Ksar Sin'),
    ('Kebili', 'Kébili - Qibili'),
    ('Kef', 'Le Kef - al-Kaf'),
    ('Mahdia', 'Mahdia - al-Mahdiya'),
    ('Manouba', 'La Manouba - al-Manubah'),
    ('Medenine', 'Medenine - Madanīn'),
    ('Monastir', 'Monastir - al-Munastir'),
    ('Nabeul', 'Nabeul - Nabul'),
    ('Sfax', 'Sfax - Safaqis'),
    ('Sidi_Bouzid', 'Sidi Bouzid - Sidi Bouzid'),
    ('Siliana', 'Siliana - Siliana'),
    ('Sousse', 'Sousse - Susa'),
    ('Tataouine', 'Tataouine - Tatawin'),
    ('Tozeur', 'Tozeur - Tūzūr'),
    ('Tunis', 'Tunis - Tunis'),
    ('Zaghouan', 'Zaghouan - Zaghouan'),
)
class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m')
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name} ({self.alt_text})"


class Order(models.Model):
    STATUS_PENDING = 'PENDING'
    STATUS_SHIPPED = 'SHIPPED'
    STATUS_DELIVERED = 'DELIVERED'
    STATUS_CANCELLED = 'CANCELLED'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'En attente'),
        (STATUS_SHIPPED, 'Expédié'),
        (STATUS_DELIVERED, 'Livré'),
        (STATUS_CANCELLED, 'Annulé'),
    )

    id = models.BigAutoField(primary_key=True)
    id_unique = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)
    address = models.TextField()
    city = models.CharField(max_length=50, choices=GOVERNORATES)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id_unique} - {self.full_name}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    selected_size = models.CharField(max_length=50, blank=True)
    selected_color = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name} @ {self.price}'
