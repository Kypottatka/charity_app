from django.contrib.auth.forms import UserCreationForm
from django import forms
from main.models import CustomUser


class CreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    is_fund = forms.BooleanField(required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username', 'is_fund')
