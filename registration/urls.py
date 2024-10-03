from django.urls import path
from .views import create_booking, search_train, confirm_booking, home , cancel_ticket

urlpatterns = [
    path('', home, name='home'),
    path('create-booking/', create_booking, name='create_booking'),
    path('search-train/', search_train, name='search_train'),
    path('cancel-ticket/', cancel_ticket, name='cancel_ticket'),
    path('confirm-booking/', confirm_booking, name='confirm_booking'),
    # Other URL patterns
]