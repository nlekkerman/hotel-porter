# forms.py
from django import forms
from guest.models import Guest


class GuestForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['first_name', 'last_name', 'email', 'days_booked', 'check_in_date', 'check_out_date', 'id_pin', 'phone_number']
