from django.forms import ModelForm
from .models import Booking
from django import forms


# Code added for loading form data on the Booking page
class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = "__all__"


class JSONUploadForm(forms.Form):
    json_file = forms.FileField(label='Select a JSON file')