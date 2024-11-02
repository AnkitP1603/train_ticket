from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import random,string
from .models import Journey, Booking, SeatBooking, Seat, Passenger, Station, Route
from .forms import SearchTrainForm
from datetime import datetime
from django.db import transaction
from django.contrib import messages

def generate_pnr(length=10):
    characters = string.ascii_uppercase + string.digits
    while True:
        pnr = ''.join(random.choice(characters) for _ in range(length))
        if not Booking.objects.filter(pnr=pnr).exists():
            return pnr


@login_required
def home(request):
    user_bookings = Booking.objects.filter(user=request.user)
    
    context = {
        'user_bookings': user_bookings
    }
    
    return render(request, 'registration/home.html', context)




@login_required
def search_train(request):
    if request.method == "POST":
        form = SearchTrainForm(request.POST)
        if form.is_valid():
            start_station = form.cleaned_data['start_station']
            dest_station = form.cleaned_data['dest_station']
            date_of_journey = form.cleaned_data['date_of_journey']
            
            available_journeys = Journey.objects.filter(
                src_station=start_station, 
                dest_station=dest_station
            ).prefetch_related('seat_set')

            return render(request, 'registration/select_train.html', {
                'journeys': available_journeys,
                'start_station': start_station,
                'dest_station': dest_station,
                'date_of_journey': date_of_journey
            })
    else:
        form = SearchTrainForm()

    return render(request, 'registration/search_train.html', {'form': form})


@login_required
def confirm_booking(request):
    if request.method == "POST":
        selected_seat_id = request.POST.get('selected_seat')
        start_station_code = request.POST.get('start_station')
        dest_station_code = request.POST.get('dest_station')
        date_of_journey = request.POST.get('date_of_journey')

        try:
            date_of_journey = datetime.strptime(date_of_journey, "%b. %d, %Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use a valid format (e.g., Oct. 18, 2024).")
            return redirect('search_train')
        
        seat = get_object_or_404(Seat, seat_id=selected_seat_id)
        start_station = get_object_or_404(Station, station_code=start_station_code)
        dest_station = get_object_or_404(Station, station_code=dest_station_code)

        try:
            start_route = Route.objects.get(train=seat.journey.train, station=start_station)
            dest_route = Route.objects.get(train=seat.journey.train, station=dest_station)
        except Route.DoesNotExist:
            messages.error(request, "Invalid route: Could not find start or destination station on this train's route.")
            return redirect('search_train')
    
        route_segments = Route.objects.filter(
            train=seat.journey.train,
            stop_order__gte=start_route.stop_order,
            stop_order__lt=dest_route.stop_order
        ).order_by('stop_order')

        available_seats = seat.carriage.seating_capacity

        for segment in route_segments:
            start = segment.station
            end = Route.objects.get(train=seat.journey.train,stop_order = segment.stop_order+1).station
            journey_segment = Journey.objects.get(train=seat.journey.train,src_station=start,dest_station=end)
            seat_segment = Seat.objects.filter(journey=journey_segment,carriage=seat.carriage)

            curr_available_seats = seat_segment.first().available_seats(date_of_journey)
            if curr_available_seats <= 0:
                messages.error(request, "No available seats for the journey!")
                return redirect('search_train')
            else:
                available_seats = min(available_seats,curr_available_seats)
            
        if available_seats > 0:
            context = {
                'seat': seat,
                'available_seats': available_seats,
                'date_of_journey': date_of_journey,
                'start_station': start_station,
                'dest_station': dest_station,
            }
            return render(request, 'registration/confirm_booking.html', context)
        else:
            messages.error(request, "No available seats for this journey.")
            return redirect('search_train')

    return redirect('search_train')
        

        


@login_required
def create_booking(request):
    if request.method == "POST":
        selected_seat_id = request.POST.get('selected_seat_id')
        start_station_code = request.POST.get('start_station_code')
        dest_station_code = request.POST.get('dest_station_code')
        date_of_journey = request.POST.get('date_of_journey')
        available_seats = request.POST.get('available_seats')

        print(f"Trying to retrieve seat with ID: {selected_seat_id}")
        seat = get_object_or_404(Seat, seat_id=selected_seat_id)
        start_station = get_object_or_404(Station, station_code=start_station_code)
        dest_station = get_object_or_404(Station, station_code=dest_station_code)
        passenger = get_object_or_404(Passenger, user=request.user)
        pnr = generate_pnr()

        try:
            date_of_journey = datetime.strptime(date_of_journey, "%b. %d, %Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use a valid format (e.g., Oct. 18, 2024).")
            return redirect('search_train')

        try:
            start_route = Route.objects.get(train=seat.journey.train, station=start_station)
            dest_route = Route.objects.get(train=seat.journey.train, station=dest_station)
        except Route.DoesNotExist:
            messages.error(request, "Invalid route: Could not find start or destination station on this train's route.")
            return redirect('search_train')
    
        route_segments = Route.objects.filter(
            train=seat.journey.train,
            stop_order__gte=start_route.stop_order,
            stop_order__lt=dest_route.stop_order
        ).order_by('stop_order')

        try:
            with transaction.atomic():
                if len(route_segments)>1:
                    for segment in route_segments:
                        start = segment.station 
                        end = Route.objects.get(train=seat.journey.train,stop_order = segment.stop_order+1).station

                        journey_segment = Journey.objects.get(train=seat.journey.train,src_station=start,dest_station=end)
                        seat_segment = Seat.objects.filter(journey=journey_segment,carriage=seat.carriage).first()

                        SeatBooking.objects.create(
                            passenger=passenger,
                            seat=seat_segment,
                            journey=journey_segment,
                            start_station=start,
                            end_station=end,
                            journey_date=date_of_journey,
                        )

                seat_booking = SeatBooking.objects.create(
                    passenger=passenger,
                    seat=seat,
                    journey=seat.journey,
                    start_station=start_station,
                    end_station=dest_station,
                    journey_date=date_of_journey,
                )

                Booking.objects.create(
                    booking=seat_booking,
                    user=request.user,
                    booking_status="Confirmed",
                    booking_date=datetime.now().date(),
                    total_amt=seat.price,
                    pnr=pnr
                )

            messages.success(request, "Booking confirmed!")
            return redirect('home')

        except Exception as e:
            messages.error(request, "Booking could not be completed: {}".format(str(e)))
            return redirect('search_train')

    messages.error(request, "Booking could not be completed.")
    return redirect('search_train')


@login_required
def cancel_ticket(request):
    if request.method == "POST":
        pnr = request.POST.get('pnr')
        confirm = request.POST.get('confirm')

        try:
            booking = Booking.objects.get(pnr=pnr)

            if confirm == 'yes':
                seat_booking = SeatBooking.objects.get(booking=booking)
                seat = seat_booking.seat
                passenger = seat_booking.passenger

                start_route = Route.objects.get(train=seat.journey.train, station=seat_booking.start_station)
                dest_route = Route.objects.get(train=seat.journey.train, station=seat_booking.end_station)

                route_segments = Route.objects.filter(
                    train=seat.journey.train,
                    stop_order__gte=start_route.stop_order,
                    stop_order__lt=dest_route.stop_order
                ).order_by('stop_order')

                if len(route_segments)>1:
                    for segment in route_segments:
                        start = segment.station 
                        end = Route.objects.get(train=seat.journey.train,stop_order = segment.stop_order+1).station

                        journey_segment = Journey.objects.get(train=seat.journey.train,src_station=start,dest_station=end)
                        seat_segment = Seat.objects.filter(journey=journey_segment,carriage=seat.carriage).first()

                        seat_booking_segment = SeatBooking.objects.filter(
                            passenger = passenger,
                            seat = seat_segment,
                            journey = journey_segment,
                            start_station = start,
                            end_station = end,
                            journey_date = seat_booking.journey_date
                        ).first()

                        seat_booking_segment.delete()

                seat_booking.delete()
                booking.delete()
                messages.success(request, f"Booking with PNR {pnr} has been successfully canceled.")
                return redirect('home')

            return render(request, 'registration/cancel_confirm.html', {'booking': booking})

        except Booking.DoesNotExist:
            messages.error(request, f"Booking with PNR {pnr} not found.")
            return redirect('cancel_ticket')

    return render(request, 'registration/cancel_ticket.html')