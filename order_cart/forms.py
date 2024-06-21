from django import forms
from .models import OrderCart


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderCart
        fields = ['first_name', 'last_name', 'email', 'address',
                  'postal_code', 'city']