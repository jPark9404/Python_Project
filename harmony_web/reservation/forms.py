from django.forms import ModelForm
from django import forms
from .models import SimpleReservation, Holiday

class SimpleReservationForm(ModelForm):
    fullname = forms.CharField(label='Full name', max_length=100)
    user_email = forms.CharField(label='Email address',max_length=254)
    phone_number = forms.CharField(label='Phone Number',max_length=100)
    reservation_date = forms.CharField(label='Reservation Date')
    reservation_time = forms.CharField(label='Reservation Time')
    num_of_people = forms.IntegerField(label='Group Size')
    
    class Meta:
        model = SimpleReservation
        fields = ['fullname', 'user_email', 'phone_number', 'reservation_date', 'reservation_time', 'num_of_people']

# class SimpleReservationForm(ModelForm):
#     class Meta:
#         model = SimpleReservation
#         fields = ['fullname', 'phone_number', 'simple_reservation_date', 'num_of_people']

class HolidayForm(ModelForm):
    class Meta:
        model = Holiday
        fields = '__all__'