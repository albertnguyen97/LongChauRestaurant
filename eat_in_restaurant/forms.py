from django import forms
from .models import Table  # Replace `.models` with the actual path to your models


class TableForm(forms.Form):
    table_choices = [(table.table_id, f'Table {table.table_id}') for table in Table.objects.filter(booked=False)]

    table = forms.ChoiceField(
        label='Select Table',
        choices=[('', 'Select a Table')] + table_choices,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )


class OrderForm(forms.Form):
    food_item = forms.CharField(label='Select Food Item', widget=forms.Select())
    quantity = forms.IntegerField(label='Quantity', min_value=1)