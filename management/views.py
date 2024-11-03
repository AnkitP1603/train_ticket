from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import StationForm, TrainForm, TrainCarriageForm, RouteForm
from registration.models import Station, Train, TrainCarriage, Route, Journey, Seat, SeatBooking, Booking, Passenger

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    is_admin_user = request.user.groups.filter(name='Admin').exists()
    return render(request, 'management/admin_dashboard.html', {'is_admin_user': is_admin_user})

@login_required
def manage_stations(request):
    if request.method == "POST" and 'add_station' in request.POST:
        form = StationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Station added successfully!")
            return redirect('manage_stations')
        else:
            messages.error(request, "Failed to add station. Please check the form.")
    
    if request.method == "POST" and 'delete_station' in request.POST:
        station_id = request.POST.get('station_id')
        if station_id:
            station = get_object_or_404(Station, pk=station_id)
            station.delete()
            messages.success(request, "Station deleted successfully!")
        else:
            messages.error(request, "Station ID not provided for deletion.")
        return redirect('manage_stations')


    form = StationForm()
    stations = Station.objects.all()
    return render(request, 'management/manage_stations.html', {'form': form, 'stations': stations})


@login_required
def manage_trains(request):
    if request.method == "POST" and 'add_train' in request.POST:
        form = TrainForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Train added successfully!")
            return redirect('manage_trains')
        else:
            messages.error(request, "Failed to add train. Please check the form.")

    if request.method == "POST" and 'delete_train' in request.POST:
        train_id = request.POST.get('train_id')
        if train_id:
            train = get_object_or_404(Train, pk=train_id)
            train.delete()
            messages.success(request, "Train deleted successfully!")
        else:
            messages.error(request, "Train ID not provided for deletion.")
        return redirect('manage_trains')

    form = TrainForm()
    trains = Train.objects.all()
    return render(request, 'management/manage_trains.html', {'form': form, 'trains': trains})


@login_required
def manage_carriages(request):
    if request.method == "POST" and 'add_carriage' in request.POST:
        form = TrainCarriageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Carriage added successfully!")
            return redirect('manage_carriages')
        else:
            messages.error(request, "Failed to add carriage. Please check the form.")

    if request.method == "POST" and 'delete_carriage' in request.POST:
        carriage_id = request.POST.get('carriage_id')
        if carriage_id:
            carriage = get_object_or_404(TrainCarriage, pk=carriage_id)
            carriage.delete()
            messages.success(request, "Carriage deleted successfully!")
        else:
            messages.error(request, "Carriage ID not provided for deletion.")
        return redirect('manage_carriages')

    form = TrainCarriageForm()
    carriages = TrainCarriage.objects.all()
    return render(request, 'management/manage_carriages.html', {'form': form, 'carriages': carriages})


@login_required
def manage_routes(request):
    if request.method == "POST" and 'add_route' in request.POST:
        form = RouteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Route added successfully!")
            return redirect('manage_routes')
        else:
            messages.error(request, "Failed to add route. Please check the form.")

    if request.method == "POST" and 'delete_route' in request.POST:
        route_id = request.POST.get('route_id')
        if route_id:
            route = get_object_or_404(Route, pk=route_id)
            route.delete()
            messages.success(request, "Route deleted successfully!")
        else:
            messages.error(request, "Route ID not provided for deletion.")
        return redirect('manage_routes')

    form = RouteForm()
    trains = Train.objects.all()
    routes_by_train = {
        train: Route.objects.filter(train=train).order_by('stop_order') for train in trains
    }
    return render(request, 'management/manage_routes.html', {
        'form': form,
        'trains': trains,
        'routes_by_train': routes_by_train,
    })



@login_required
def view_journeys(request):
    journeys = Journey.objects.all()  
    return render(request, 'management/view_journeys.html', {'journeys': journeys})

@login_required
def view_seats(request):
    seats = Seat.objects.all()  
    return render(request, 'management/view_seats.html', {'seats': seats})

@login_required
def view_seat_bookings(request):
    seat_bookings = SeatBooking.objects.all()  
    return render(request, 'management/view_seat_bookings.html', {'seat_bookings': seat_bookings})

@login_required
def view_bookings(request):
    bookings = Booking.objects.all()  
    return render(request, 'management/view_bookings.html', {'bookings': bookings})

@login_required
def view_passengers(request):
    passengers = Passenger.objects.all()  
    return render(request, 'management/view_passengers.html', {'passengers': passengers})
