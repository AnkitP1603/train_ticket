from django.urls import path
from .views import create_booking, search_train, home , cancel_ticket

urlpatterns = [
    path('', home, name='home'),
    path('search-train/', search_train, name='search_train'),
    path('cancel-ticket/', cancel_ticket, name='cancel_ticket'),
    path('create-booking/', create_booking, name='create_booking'),
    # Other URL patterns
]