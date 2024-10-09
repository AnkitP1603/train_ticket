# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_id = models.AutoField(primary_key=True)
    passenger_name = models.CharField(max_length=255, verbose_name="Passenger Name")
    email = models.EmailField(unique=True, max_length=255, help_text="Enter a valid email address.")
    phone_number = models.CharField(max_length=15, help_text="Enter your phone number.")
    age = models.IntegerField(null=False, validators=[MinValueValidator(0)], help_text="Age must be a non-negative integer.")

    class Meta:
        db_table = 'passenger'
        verbose_name_plural = "Passengers"

    def __str__(self):
        return self.passenger_name



class Station(models.Model):
    station_id = models.AutoField(primary_key=True)
    station_code = models.CharField(max_length=10)
    station_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'station'

    def __str__(self):
        return self.station_code



class Train(models.Model):
    train_id = models.IntegerField(primary_key=True)
    train_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'train'

    def __str__(self):
        return self.train_name
    


class TrainCarriage(models.Model):
    carriage_id = models.AutoField(primary_key=True)
    train = models.ForeignKey(Train, models.CASCADE)
    class_name = models.CharField(max_length=10)
    seating_capacity = models.IntegerField(null=False)

    class Meta:
        db_table = 'train_carriage'

    def __str__(self):
        return f'{self.train_id} {self.class_name}'



class Journey(models.Model):
    journey_id = models.AutoField(primary_key=True)
    train = models.ForeignKey('Train', models.CASCADE)
    src_station = models.ForeignKey('Station', models.CASCADE)
    dest_station = models.ForeignKey('Station', models.CASCADE, related_name='journey_dest_station_set')
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    class Meta:
        db_table = 'journey'

    def __str__(self):
        return f'{self.src_station} to {self.dest_station} by {self.train_id}'



class Route(models.Model):
    train = models.ForeignKey('Train', models.CASCADE, blank=True, null=True)
    station = models.ForeignKey('Station', models.CASCADE, blank=True, null=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    stop_order = models.IntegerField()

    class Meta:
        db_table = 'route'

    def __str__(self):
        return f'{self.train_id} at {self.station}'


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    journey = models.ForeignKey(Journey, models.CASCADE)
    carriage = models.ForeignKey('TrainCarriage', models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.IntegerField()

    class Meta:
        db_table = 'seat'

    def __str__(self):
        return f'{self.journey} {self.carriage}'

class SeatBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    start_station = models.ForeignKey('Station', on_delete=models.CASCADE)
    end_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='seatbooking_end_station_set')

    class Meta:
        db_table = 'seat_booking'

    def __str__(self):
        return f'Booking {self.booking_id} for {self.passenger.passenger_name}'


class Booking(models.Model):
    booking = models.OneToOneField('SeatBooking', on_delete=models.CASCADE, primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    booking_status = models.CharField(max_length=255)
    booking_date = models.DateField()
    total_amt = models.DecimalField(max_digits=10, decimal_places=2)
    pnr = models.CharField(unique=True, max_length=15)
    date_of_journey = models.DateField(null=True)

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f'Booking {self.pnr} by {self.user.username}'









