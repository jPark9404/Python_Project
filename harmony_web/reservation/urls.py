from django.urls import path
from . import views

urlpatterns = [
    #path('main/', views.room, name="main"),

    path('', views.createSimpleReservation, name="simple_reservation"),
    path('confirm/<str:pk>/', views.confirm_email, name="confirm_reservation"),
    path('delete/<str:pk>/', views.delete_reservation, name="delete_reservation"),
    path('email/', views.send_email, name="email_reservation"),
    # path('', views.createReservation, name="reservation"),

    path('holidays/', views.get_holidays, name="holidays"),
    path('create-holiday/', views.create_holiday, name="create-holiday"),

    path('day-details/<str:dt>/', views.DayDetailView, name="get_day"),
]