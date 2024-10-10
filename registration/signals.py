from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Passenger

@receiver(post_save, sender=User)
def create_passenger(sender, instance, created, **kwargs):
    if created:
        Passenger.objects.create(
            user=instance, 
            passenger_name=instance.username, 
            email=instance.email, 
            age=0  
        )
        

