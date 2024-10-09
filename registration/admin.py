from django.contrib import admin
#from .models import Booking, Schedule

# admin.site.register(Schedule)

# @admin.register(Booking)
# class BookingAdmin(admin.ModelAdmin):
#     list_display = ('user', 'train_name', 'start_station', 'dest_station', 'pnr', 'booking_status')
#     search_fields = ('user__username', 'train_name', 'pnr')
#     list_filter = ('booking_status', 'user')

from .models import Passenger, Station, Train, TrainCarriage, Journey, Route, Seat, SeatBooking, Booking

admin.site.register(Passenger)
admin.site.register(Station)
admin.site.register(Train)
admin.site.register(TrainCarriage)
admin.site.register(Journey)
admin.site.register(Route)
admin.site.register(Seat)
admin.site.register(SeatBooking)
admin.site.register(Booking)

