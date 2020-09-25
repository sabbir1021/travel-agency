from django import forms 
from .models import Booking , Location
from django.conf import settings

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'name',
            'email',
            'phone',
            'message'
        ]


class FilterForm(forms.Form):
    PRICE_CHOICES = (
        ('0', 'Price Range'),
        ('500', 'Up To 500'),
        ('1000', 'Up To 1000'),
        ('5000', 'Up To 5000'),
        ('inf', 'Greater Than 5000'),
    )
    price_range = forms.ChoiceField(
        label="", choices=PRICE_CHOICES, required=False)
    title = forms.CharField(
        label="", required=False)
    date = forms.DateField(
        label="", required=False,
        widget=forms.TextInput(attrs={'type': 'date'})
                )
    city = forms.ModelChoiceField(
        label="",queryset=Location.objects.values_list('city', flat=True).distinct(), required=False)