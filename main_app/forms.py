
from django.contrib.auth.models import User, Account
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm


class AccountCreate(ModelForm):
    class Meta:
        model =  Account
        fields = ['picture']



class EditProfileForm(UserChangeForm):
    
    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'username',
            'password'
        )

        