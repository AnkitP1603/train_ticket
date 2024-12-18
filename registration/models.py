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
from datetime import datetime, timedelta


class Passenger(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    passenger_id = models.AutoField(primary_key=True)
    passenger_name = models.CharField(max_length=255, verbose_name="Passenger Name")
    email = models.EmailField(unique=True,max_length=255, help_text="Enter a valid email address.")
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
    base_rate = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

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

    def get_duration(self):
        start = datetime.combine(datetime.min, self.departure_time)
        end = datetime.combine(datetime.min, self.arrival_time)
        if end < start:
            end += timedelta(days=1) 

        duration = end - start
        total_minutes = duration.total_seconds() // 60
        hours, minutes = divmod(total_minutes, 60)

        formatted_duration = f"{int(hours)}hrs:{int(minutes)}mins"
        total_hours = hours + (minutes / 60) 
        return formatted_duration, total_hours



class Route(models.Model):
    train = models.ForeignKey('Train', models.CASCADE, blank=True, null=True)
    station = models.ForeignKey('Station', models.CASCADE, blank=True, null=True)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    stop_order = models.IntegerField()

    class Meta:
        db_table = 'route'

    def __str__(self):
        return f'{self.train.train_id} at {self.station}'


class Seat(models.Model):
    seat_id = models.AutoField(primary_key=True)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    carriage = models.ForeignKey('TrainCarriage', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2) 

    class Meta:
        db_table = 'seat'
        unique_together = ('journey', 'carriage') 

    def __str__(self):
        return f'{self.journey} {self.carriage}'
    
    def available_seats(self, date):
        total_capacity = self.carriage.seating_capacity
        booked_seats = SeatBooking.objects.filter(seat=self, journey=self.journey, seat__carriage=self.carriage, journey_date=date).count()
        return total_capacity - booked_seats


class SeatBooking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    start_station = models.ForeignKey('Station', on_delete=models.CASCADE)
    end_station = models.ForeignKey('Station', on_delete=models.CASCADE, related_name='seatbooking_end_station_set')
    journey_date = models.DateField(null=False)

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
    

    class Meta:
        db_table = 'booking'

    def __str__(self):
        return f'Booking {self.pnr} by {self.user.username}'









