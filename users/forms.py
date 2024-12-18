from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    age = forms.IntegerField(required=True, min_value=0)

    class Meta:
        model = User
        fields = ['username','email','password1','password2','age']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use. Please use a different email address.")
        return email



class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['age','image']
        


class CheckPnrForm(forms.Form):
    pnr = forms.CharField(label='PNR Number', max_length=100)


class TrainIDForm(forms.Form):
    train_id = forms.IntegerField(label='Enter Train ID', min_value=1)
