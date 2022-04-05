from django.forms import ModelForm
from .models import Account

class AccountCreate(ModelForm):
    class Meta:
        model =  Account
        fields = ['picture']
        