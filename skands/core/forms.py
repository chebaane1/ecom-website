from django import forms
from .models import Order, GOVERNORATES, Product


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


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True


class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        widget=MultipleFileInput(attrs={'multiple': True, 'class': 'hidden', 'id': 'image-upload-input'}),
        required=False,
        label="Ajouter des images"
    )

    class Meta:
        model = Product
        fields = ('name', 'category', 'description', 'price', 'old_price', 'is_active')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 focus:outline-none transition'}),
            'category': forms.Select(attrs={'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 focus:outline-none transition'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 focus:outline-none transition'}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 focus:outline-none transition'}),
            'old_price': forms.NumberInput(attrs={'step': '0.01', 'class': 'w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 focus:outline-none transition'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'rounded text-red-600 focus:ring-red-500 h-5 w-5 cursor-pointer'}),
        }

