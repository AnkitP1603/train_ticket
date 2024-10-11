from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import random,string
from .models import Journey, Booking, SeatBooking, Seat, Passenger, Station
from .forms import SearchTrainForm
from datetime import datetime
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
            
            available_trains = Journey.objects.filter(
                src_station=start_station, 
                dest_station=dest_station
            ).prefetch_related('seat_set')

            return render(request, 'registration/select_train.html', {
                'trains': available_trains,
                'start_station': start_station,
                'dest_station': dest_station,
                'date_of_journey': date_of_journey
            })
    else:
        form = SearchTrainForm()

    return render(request, 'registration/search_train.html', {'form': form})


@login_required
def create_booking(request):
    if request.method == "POST":
        selected_seat_id = request.POST.get('selected_seat')
        start_station = request.POST.get('start_station')
        dest_station = request.POST.get('dest_station')
        date_of_journey = request.POST.get('date_of_journey')

        try:
            date_of_journey = datetime.strptime(date_of_journey, "%b. %d, %Y").date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use a valid format (e.g., Oct. 18, 2024).")
            return redirect('search_train')

        seat = get_object_or_404(Seat, seat_id=selected_seat_id)

        if request.user.is_authenticated:
            if seat.available_seats <= 0:
                messages.error(request, "No available seats!")
                return redirect('search_train')
            
            passenger = get_object_or_404(Passenger,user=request.user)
            pnr = generate_pnr()

            try:
                seat_booking = SeatBooking.objects.create(
                    passenger=passenger,
                    seat=seat,
                    journey=seat.journey, 
                    start_station=get_object_or_404(Station,station_code = start_station),
                    end_station=get_object_or_404(Station,station_code = dest_station)
                )

                booking = Booking.objects.create(
                    booking=seat_booking,  
                    user=request.user,
                    booking_status="Confirmed",
                    booking_date=datetime.now().date(), 
                    total_amt=seat.price,
                    date_of_journey=date_of_journey,
                    pnr=pnr
                )

                seat.available_seats -= 1
                seat.save()

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
            booking = get_object_or_404(Booking, pnr=pnr)

            if confirm == 'yes':
                seat_booking = SeatBooking.objects.get(booking=booking)
                seat = seat_booking.seat
                seat.available_seats += 1
                seat.save()
                seat_booking.delete()
                booking.delete()
                messages.success(request, f"Booking with PNR {pnr} has been successfully canceled.")
                return redirect('home')

            return render(request, 'registration/cancel_confirm.html', {'booking': booking})

        except Booking.DoesNotExist:
            messages.error(request, f"Booking with PNR {pnr} not found.")
            return redirect('cancel_ticket')

    return render(request, 'registration/cancel_ticket.html')