from django.urls import path
from .views import create_booking, search_train, home , cancel_ticket, confirm_booking

urlpatterns = [
    path('', home, name='home'),
    path('search-train/', search_train, name='search_train'),
    path('cancel-ticket/', cancel_ticket, name='cancel_ticket'),
    path('create-booking/', create_booking, name='create_booking'),
    path('confirm-booking/', confirm_booking, name='confirm_booking'),
    path('home/', home, name='home'), 

    # Other URL patterns
]