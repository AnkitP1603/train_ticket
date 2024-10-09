from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile

# Create your views here.

def about(request):
    return render(request, 'users/about.html',{'title':'About'})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


def user_logout(request):
    logout(request)
    return render(request, 'users/logout.html', {})



def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            
            # Ensure profile exists
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            
            return redirect('home')  # or redirect to your desired page
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})



@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }
    return render(request,'users/profile.html',context)




import calendar
from datetime import datetime

def calendar_view(request):
    # Get the current month and year
    now = datetime.now()
    day = now.day
    month = now.month
    year = now.year

    # Create a calendar for the current month
    cal = calendar.monthcalendar(year, month)

    context = {
        'year': year,
        'month': month,
        'day': day,
        'calendar': cal,
        'month_name': calendar.month_name[month],
    }

    return render(request, 'users/calendar.html', context)


from registration.models import Booking,SeatBooking,Journey
from .forms import CheckPnrForm
def check_pnr(request):
    if request.method == 'POST':
        form = CheckPnrForm(request.POST)
        if form.is_valid():
            pnr = form.cleaned_data['pnr']
            try:
                booking = Booking.objects.get(pnr=pnr)
                seat_booking = SeatBooking.objects.select_related('journey').get(booking=booking)
                journey = seat_booking.journey
                seat = seat_booking.seat

                context = {
                    'booking': booking,
                    'seat_booking': seat_booking,
                    'journey': journey,
                    'seat': seat,
                }

                return render(request, 'users/check_pnr.html',context)
            except Booking.DoesNotExist:
                messages.error(request, 'No booking found with the provided PNR.')
    else:
        form = CheckPnrForm()
    
    return render(request, 'users/check_pnr.html', {'form': form})