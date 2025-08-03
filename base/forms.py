from django.forms import ModelForm
from .models import Room

from django.contrib.auth import get_user_model
User = get_user_model()

from django.contrib.auth.forms import UserCreationForm


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields = '__all__'
        exclude = ['host', 'participants']


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']


class UserForm(ModelForm):
    class Meta:
        model=User
        fields = ['avatar', 'name', 'username', 'email', 'bio']