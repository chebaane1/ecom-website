from django import forms
# pyrefly: ignore [missing-import]
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


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = []
            for d in data:
                if d and getattr(d, 'name', '') == '' and getattr(d, 'size', 0) == 0:
                    continue
                result.append(single_file_clean(d, initial))
            return result
        else:
            if data and getattr(data, 'name', '') == '' and getattr(data, 'size', 0) == 0:
                return None
            return single_file_clean(data, initial)


class ProductForm(forms.ModelForm):
    images = MultipleImageField(
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

