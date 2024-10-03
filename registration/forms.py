from django import forms
from .models import Booking,Schedule

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['train_name', 'pnr', 'booking_status', 'date_of_journey', 'start_station', 'dest_station']  # Ensure 'train' is included

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Extract user if provided
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
    

class SearchTrainForm(forms.Form):
    start_station = forms.CharField(label="Departure Station", max_length=100)
    dest_station = forms.CharField(label="Destination Station", max_length=100)


class CancelTicketForm(forms.Form):
    pnr = forms.CharField(label='PNR Number', max_length=100)