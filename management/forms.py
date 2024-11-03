from django import forms
from registration.models import Station,Train,TrainCarriage,Route
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class StationForm(forms.ModelForm):
    class Meta:
        model = Station
        fields = ['station_code', 'station_name']


class TrainForm(forms.ModelForm):
    class Meta:
        model = Train
        fields = ['train_id','train_name']
        labels = {
            'train_name': 'Train Name',
            'train_id' : 'Train Number'
        }


class TrainCarriageForm(forms.ModelForm):
    class Meta:
        model = TrainCarriage
        fields = ['train', 'class_name', 'seating_capacity', 'base_rate']
        labels = {
            'train': 'Train',
            'class_name': 'Class Name',
            'seating_capacity': 'Seating Capacity',
            'base_rate': 'Base Rate',
        }


class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['train', 'station', 'departure_time', 'arrival_time', 'stop_order']
        labels = {
            'train': 'Train',
            'station': 'Station',
            'departure_time': 'Departure Time',
            'arrival_time': 'Arrival Time',
            'stop_order': 'Stop Order',
        }
        widgets = {
            'departure_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }