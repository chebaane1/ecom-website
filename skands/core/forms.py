from django import forms
from .models import Order, GOVERNORATES


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'address', 'city')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'city': forms.Select(choices=GOVERNORATES),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status',)
