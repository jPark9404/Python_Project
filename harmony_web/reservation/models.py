# from account.models import User
from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime    
# Create your models here.

"""Creating a simple reservation"""
class SimpleReservation(models.Model):
    fullname = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=254, blank=True, null=True)
    # phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(max_length=17, blank=True) # Validators should be a list (555) 555 - 5555
    reservation_date = models.CharField(max_length=15, blank=True, null=True)
    reservation_time = models.CharField(max_length=9, blank=True, null=True)
    confirmed = models.CharField(max_length=1, blank=True, null=True)
    num_of_people = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)], default=2)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.fullname + " Phone Number: " + self.phone_number + " Date: " + str(self.created)

"""Reservation day model represeting single day and free/non-free spots for that day"""
class ReservationDay(models.Model):
    date = models.DateField(null=False, blank=False)
    spots_total = models.IntegerField(null=True, default=32)
    spots_free = models.IntegerField(null=True, default=32)

    def __str__(self):
        return str(self.date) + " Total: " + str(self.spots_total) + " Free: " + str(self.spots_free)

"""Days that are free from work"""
class Holiday(models.Model):
    name = models.CharField(max_length=100, blank=True)
    date = models.DateField(null=False, blank=False)
    active = models.BooleanField(default=True, editable=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return str(self.name) + " " + str(self.date)


class DayTime1(models.Model):
    day = models.CharField(max_length=15)
    time = models.CharField(max_length=9)

