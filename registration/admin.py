from django.contrib import admin
from .models import Booking, Schedule

admin.site.register(Schedule)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'train_name', 'start_station', 'dest_station', 'pnr', 'booking_status')
    search_fields = ('user__username', 'train_name', 'pnr')
    list_filter = ('booking_status', 'user')
