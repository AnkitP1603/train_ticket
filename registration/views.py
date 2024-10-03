from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import random,string
from .models import Schedule, Booking
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
def create_booking(request):
    if request.method == "POST":
        # Assuming form data includes start_station, dest_station, etc.
        start_station = request.POST.get('start_station')
        dest_station = request.POST.get('dest_station')
        date_of_journey = request.POST.get('date_of_journey')

        train = get_object_or_404(Schedule, id=request.POST.get('train_id'))
        
        if request.user.is_authenticated:
            pnr = generate_pnr()  # Assume this is your PNR generation method
            booking = Booking.objects.create(
                user=request.user,
                train_name=train,
                start_station=start_station,
                dest_station=dest_station,  # Ensure this field is populated
                date_of_journey=date_of_journey,
                booking_status="Confirmed",
                pnr=pnr
            )
            return redirect('home')


@login_required
def home(request):
    # Fetch bookings for the current user
    user_bookings = Booking.objects.filter(user=request.user).select_related('train_name')
    
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

            # Filter available trains based on start and end stations
            available_trains = Schedule.objects.filter(start_station=start_station, dest_station=dest_station)

            return render(request, 'registration/select_train.html', {
                'trains': available_trains,
                'start_station': start_station,
                'dest_station': dest_station,
            })
    else:
        form = SearchTrainForm()

    return render(request, 'registration/search_train.html', {'form': form})



def confirm_booking(request):
    if request.method == "POST":
        train_id = request.POST.get('train_id')
        start_station = request.POST.get('start_station')
        dest_station = request.POST.get('dest_station')
        date_of_journey = request.POST.get('date_of_journey')

        try:
            date_of_journey = datetime.strptime(date_of_journey, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format. Please use YYYY-MM-DD format.")
            return redirect('select_train')
        # Fetch the selected train
        train = get_object_or_404(Schedule, id=train_id)

        # Create a new booking
        if request.user.is_authenticated:
            pnr = generate_pnr()
            booking = Booking.objects.create(
                user=request.user,
                train_name=train,
                start_station=start_station,
                dest_station=dest_station,
                date_of_journey=date_of_journey,
                booking_status="Confirmed",
                pnr=pnr
            )
            messages.success(request, "Booking confirmed!")
            return redirect('home')

    return redirect('search_train')




@login_required
def cancel_ticket(request):
    if request.method == "POST":
        pnr = request.POST.get('pnr')
        confirm = request.POST.get('confirm')

        try:
            # Get the booking based on the PNR
            booking = get_object_or_404(Booking, pnr=pnr)

            if confirm == 'yes':  # If the user confirmed, delete the booking
                booking.delete()
                messages.success(request, f"Booking with PNR {pnr} has been successfully canceled.")
                return redirect('home')

            # Render the confirmation page if not confirmed yet
            return render(request, 'registration/cancel_confirm.html', {'booking': booking})

        except Booking.DoesNotExist:
            messages.error(request, f"Booking with PNR {pnr} not found.")
            return redirect('cancel_ticket')

    return render(request, 'registration/cancel_ticket.html')