from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import SimpleReservationForm, HolidayForm
import datetime
from itertools import chain
from django.shortcuts import get_object_or_404
##
import google
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create your views here.
def createSimpleReservation(request):
    """Users without an account and create a reservation"""
    form = SimpleReservationForm()
    max_group_size = 10
    options_group_size = max_group_size

    today = datetime.date.today()
    
    if request.method == 'POST':
        form = SimpleReservationForm(request.POST)
        if form.is_valid():
            reservation_date = form.cleaned_data['reservation_date']
            
            # check if the day is valid
            print('reservation date:::')
            print(reservation_date)
            res_date = datetime.datetime.strptime(reservation_date, "%Y-%m-%d").date()
            if res_date < today:
                return HttpResponse("You can not make reservations on days that have passed")

            # Check if it is not a holiday day
            if Holiday.objects.filter(date=reservation_date, active=True).count() != 0:
                return HttpResponse("You can not make reservations on holidays")

            # Check if spot is still available
            reservation_day = ReservationDay.objects.get_or_create(date=reservation_date)
            reservation_day = ReservationDay.objects.get(date=reservation_date)
            print('Reservation Day:')
            aa = reservation_day.spots_free
            print(aa)
            if reservation_day.spots_free < 1:
                return HttpResponse("No spots free or reservation closed")

            if reservation_day.spots_free < max_group_size:
                options_group_size = reservation_day.spots_free
            else:
                options_group_size = max_group_size
            # Decrement counter on Reservation Day
            reservation_day.spots_free = reservation_day.spots_free-1
            reservation_day.save()

            # Create reservation using current model
            reserv = form.save()

            #Send email for confirmation
            email_list = [
                reserv.user_email
            ]
            send_test_emails(email_list[0], reserv.created)
            return redirect('email_reservation')
        else:
            messages.error(request, 'An error occurred during registration')

    available_time = DayTime1.objects.filter(day='Saturday')
        
    context ={
        'form': form, 
        'today': today,
        'options_group_size': range(1, options_group_size+1),
        'available_time': available_time
        }
    return render(request, 'reservation/reservation_form.html', context)


def send_email(request):
    header = "An email has been sent!"
    body="Thank you for making a reservation! "
    message="Please follow the details on the email to confirm your reservation"
    context = {'header': header, 'body': body, 'message': message}
    return render(request, 'reservation/resevation_messages.html', context)


def confirm_email(request, pk):
    reserve= get_object_or_404(SimpleReservation, created=pk)
    if reserve.confirmed == 'Y':
        context = {'reserve': reserve}
        return render(request, 'reservation/confirm_reservation.html', context)
    
    
    time_now = datetime.datetime.now(tz=None)
    time_created = reserve.created.replace(tzinfo=None)
    
    dt = time_now - time_created

    if dt.seconds /60/60 > 19:
        reserve_date = reserve.reservation_date
        reserve_time = reserve.reservation_time
        header = "Your confirmation time has expired."
        body="Plase make a new reservation"
        message="Reservation date and time: " + str(reserve_date) + " " + str(reserve_time)
        context = {'header': header, 'body': body, 'message': message}
        return render(request, 'reservation/resevation_messages.html', context)

    reserve.confirmed = 'Y'
    reserve.save()
    context = {'reserve': reserve}
    return render(request, 'reservation/confirm_reservation.html', context)

def delete_reservation(request, pk):
    reserve = SimpleReservation.objects.get(created=pk)
    reserve_date = reserve.reservation_date
    reserve_time = reserve.reservation_time
    reserve.delete() 
    header = "Reservation Deleted Successfully!"
    body="Yor reservation with the following information has successfully been deleted"
    message="Reservation date and time: " + str(reserve_date) + " " + str(reserve_time)
    context = {'header': header, 'body': body, 'message': message}
    return render(request, 'reservation/resevation_messages.html', context)


@login_required(login_url='login')
def create_holiday(request):
    """Get holiday days in particular year"""
    form = HolidayForm()
    if request.user.is_superuser:
        if request.method == 'POST':
            form = HolidayForm(request.POST)
            if form.is_valid:
                form.save()
                """get the reservations for that date & send an SMS for the cancelation"""
                context={'form': form}
                return render(request, 'reservation/holiday_form.html', context)
    else:
        return HttpResponse('You are not allowed here!')

    context={'form': form}
    return render(request, 'reservation/holiday_form.html', context)


def get_holidays(request):
    """Get holiday days in particular year"""
    # date = int(request.GET['date'])
    # holidays = Holiday.objects.filter(
    #         date__gte=date,
    #         date__lte=date)
    holidays = Holiday.objects.all()
    context={'holidays': holidays}
    return render(request, 'reservation/holiday.html', context)


def DayDetailView(request, dt):
     """Get available spots for a day"""
     reserv_date = ReservationDay.objects.get(date=dt)
     context = {'reserv_date': reserv_date}
     return render(request, 'reservation/day_details.html', context)



def Create_Service(client_secret_file, api_name, api_version, *scopes):
    # print(client_secret_file, api_name, api_version, scopes, sep='-')
    SCOPES = [scope for scope in scopes[0]]
    # print(SCOPES)

    cred = None

    pickle_file = f'{api_name}_{api_version}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        # print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def send_test_emails(email, id):
    CLIENT_SECRET_FILE = 'reservation/client_secret.json'
    API_NAME = 'gmail'
    API_VERSION = 'v1'
    SCOPES = ['https://mail.google.com/']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    
    email_body = '<p>Thank you for making a reservation with us.<br>To confirm your reservation please click <a href="http://127.0.0.1:8000/reservation/confirm/' + str(id) + '/" >here</a><br>Thanks,<br>Harmony Restaurant<br>202 17 Ave SE, Calgary, <br>AB T2G 1H4<br><a href="https://harmony-restaurant.ca/" >harmony-restaurant.ca<a></p>'

    # msg = MIMEText(email_body ,'html')

    emailMsg = email_body
    mimeMessage = MIMEMultipart()
    mimeMessage['to'] = email
    mimeMessage['subject'] = 'Confirm your reservation!'
    mimeMessage.attach(MIMEText(emailMsg, 'html'))
    raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

    message = service.users().messages().send(userId='me', body={'raw': raw_string}).execute()
    
