# eat_in_app/forms.py
from django import forms


class TableForm(forms.Form):
    table = forms.CharField(label='Select Table', widget=forms.Select(choices=[('table1', 'Table 1'), ('table2', 'Table 2')]))


class OrderForm(forms.Form):
    food_item = forms.CharField(label='Select Food Item', widget=forms.Select())
    quantity = forms.IntegerField(label='Quantity', min_value=1)