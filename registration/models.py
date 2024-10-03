from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Schedule(models.Model):
    train_name = models.CharField(max_length=100)
    start_station = models.CharField(max_length=100)
    dest_station = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.train_name}: {self.start_station} to {self.dest_station}"



class Booking(models.Model):
    TRAIN_CHOICES = [
        ('Train A', 'Train A'),
        ('Train B', 'Train B'),
        ('Train C', 'Train C'),
        # Add more train options here
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    train_name = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    start_station = models.CharField(max_length=100)  # Added field
    dest_station = models.CharField(max_length=100)
    pnr = models.CharField(max_length=20, unique=True)  # Unique PNR for each booking
    booking_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    date_of_journey = models.DateField(default=timezone.now) 
    
    def __str__(self):
        return f"{self.train_name} - {self.start_station} to {self.dest_station} on {self.date_of_journey}"
    





