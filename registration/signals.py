from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from decimal import Decimal
from django.contrib.auth.models import User
from .models import Route,Journey,Passenger,Seat,TrainCarriage
from users.models import Profile


@receiver(post_save, sender=Route)
def create_journeys_on_route_creation(sender, instance, created, **kwargs):
    if created:
        print("Signal triggered: A new Route has been added.")
        train = instance.train
        routes = Route.objects.filter(train=train).order_by('stop_order')

        for i in range(len(routes)):
            for j in range(i + 1, len(routes)):
                src_station = routes[i].station
                dest_station = routes[j].station
                departure_time = routes[i].departure_time
                arrival_time = routes[j].arrival_time

                journey_exists = Journey.objects.filter(
                    train=train,
                    src_station=src_station,
                    dest_station=dest_station
                ).exists()

                if not journey_exists:
                    Journey.objects.create(
                        train=train,
                        src_station=src_station,
                        dest_station=dest_station,
                        departure_time=departure_time,
                        arrival_time=arrival_time
                    )



@receiver(post_save, sender=Journey)
def create_seats_for_new_journey(sender, instance, created, **kwargs):
    if created:
        carriages = TrainCarriage.objects.filter(train=instance.train)

        for carriage in carriages:
            formatted_duration, total_hours = instance.get_duration()
            dynamic_price = carriage.base_rate * Decimal(total_hours)

            Seat.objects.create(
                journey=instance,
                carriage=carriage,
                price=dynamic_price,
            )
            print(f"Seat created for carriage {carriage} with duration {formatted_duration} and price {dynamic_price}")


@receiver(post_delete, sender=Route)
def delete_journeys_and_seats_on_route_deletion(sender, instance, **kwargs):
    print("Signal triggered: A Route has been deleted.")
    station_to_remove = instance.station
    train = instance.train

    journeys_to_delete = Journey.objects.filter(train=train).filter(
        src_station=station_to_remove
    ) | Journey.objects.filter(train=train).filter(
        dest_station=station_to_remove
    )

    for journey in journeys_to_delete:
        Seat.objects.filter(journey=journey).delete()
        print(f"Deleted seats for journey from {journey.src_station} to {journey.dest_station}.")

        journey.delete()
        print(f"Deleted journey from {journey.src_station} to {journey.dest_station}.")