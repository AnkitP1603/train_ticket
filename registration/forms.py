from django import forms
from .models import Booking,Journey,Station


class SearchTrainForm(forms.Form):
    start_station = forms.ModelChoiceField(queryset=Station.objects.all(), label="Start Station", required=True)
    dest_station = forms.ModelChoiceField(queryset=Station.objects.all(), label="Destination Station", required=True)
    date_of_journey = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date of Journey",
        required=True
    )

class CancelTicketForm(forms.Form):
    pnr = forms.CharField(label='PNR Number', max_length=100)