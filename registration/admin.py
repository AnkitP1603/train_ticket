from django.contrib import admin
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

