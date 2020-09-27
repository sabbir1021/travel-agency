from django import forms
from .models import Booking, Location, Package, City
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


class FilterForm(forms.ModelForm):
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

    class Meta:
        model = Location
        fields = ('division', 'city')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = Location.objects.none()

        if 'division' in self.data:
            try:
                division_id = int(self.data.get('division'))
                self.fields['city'].queryset = City.objects.filter(
                    division_id=division_id).order_by('name')
            except (ValueError, TypeError):
                print('cathc')
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['city'].queryset = self.instance.division.city_set.order_by(
                'name')
