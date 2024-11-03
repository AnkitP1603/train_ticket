from django.urls import path
from . import views

urlpatterns = [
    path('stations/',views.manage_stations,name='manage_stations'),
    path('routes/', views.manage_routes, name='manage_routes'),
    path('trains/', views.manage_trains, name='manage_trains'),
    path('carriages/', views.manage_carriages, name='manage_carriages'),
    path('journeys/', views.view_journeys, name='view_journeys'),
    path('seats/', views.view_seats, name='view_seats'),
    path('seat_bookings/', views.view_seat_bookings, name='view_seat_bookings'),
    path('bookings/', views.view_bookings, name='view_bookings'),
    path('passengers/', views.view_passengers, name='view_passengers'),
    path('administration/', views.admin_dashboard, name='admin_dashboard'),
]