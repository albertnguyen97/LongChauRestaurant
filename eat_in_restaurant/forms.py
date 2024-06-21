from django import forms
from .models import Table  # Replace `.models` with the actual path to your models


class TableForm(forms.Form):
    selected_table = forms.IntegerField(widget=forms.HiddenInput())


class OrderForm(forms.Form):
    food_item = forms.CharField(label='Select Food Item', widget=forms.Select())
    quantity = forms.IntegerField(label='Quantity', min_value=1)