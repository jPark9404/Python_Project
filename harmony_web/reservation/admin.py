from django.contrib import admin
from .models import Holiday, SimpleReservation, ReservationDay, DayTime1

# Register your models here.
# admin.site.register(Reservation)
admin.site.register(SimpleReservation)
admin.site.register(ReservationDay)
admin.site.register(Holiday)
admin.site.register(DayTime1)

# @admin.register(SimpleReservation)
# class SimpleReservation(admin.ModelAdmin):
#     list_display = ['fullname', 'phone_number', 'date', 'num_of_people', 'updated', 'created']