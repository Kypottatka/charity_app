from django import forms
from django.forms.widgets import MultiWidget, Select
from django.core.files.images import get_image_dimensions
from .models import (
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
    CommentFund,
    CommentNonprofit,
    CommentVolunteer,
    CustomUser,
    Donation,
    UserProfile,
    FundProfile
)


class ExpiryDateInput(MultiWidget):
    def __init__(self, years, attrs=None):
        month_choices = [
            (1, 'January'), (2, 'February'), (3, 'March'),
            (4, 'April'), (5, 'May'), (6, 'June'),
            (7, 'July'), (8, 'August'), (9, 'September'),
            (10, 'October'), (11, 'November'), (12, 'December')
        ]
        widgets = (
            Select(attrs=attrs, choices=month_choices),
            Select(attrs=attrs, choices=[
                (str(x), str(x)) for x in range(years[0], years[1] + 3)]),
        )
        super().__init__(widgets, attrs)

    def format_output(self, rendered_widgets):
        return f"{rendered_widgets[0]}{rendered_widgets[1]}"

    def decompress(self, value):
        if value:
            return value.split('-')
        return [None, None]


class UpdateBalanceForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True
    )
    card_number = forms.CharField(
        min_length=16,
        max_length=16,
        widget=forms.TextInput(attrs={'placeholder': 'Card Number'}),
        required=True
    )
    card_holder = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Cardholder Name'}),
    )
    expiry_date = forms.CharField(
        widget=ExpiryDateInput(years=(2023, 2031)),
        label='Expiration Date',
    )
    cvv = forms.CharField(
        min_length=3,
        max_length=4,
        widget=forms.TextInput(attrs={'placeholder': 'CVV'}),
        required=True
    )


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'location')
        widgets = {
            'avatar': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            width, height = get_image_dimensions(avatar)
            if not (width and height):
                raise forms.ValidationError("File is not an image.")
        return avatar


class EditFundProfileForm(forms.ModelForm):
    class Meta:
        model = FundProfile
        fields = ('name', 'avatar', 'description')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(
                attrs={'class': 'form-control-file'}),
            'description': forms.Textarea(attrs={'class': 'form-control'})
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            width, height = get_image_dimensions(avatar)
            if not (width and height):
                raise forms.ValidationError("File is not an image.")
        return avatar


class CommentFundForm(forms.ModelForm):
    class Meta:
        model = CommentFund
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

        labels = {
            'text': 'Your comment',
        }


class CommentNonprofitForm(forms.ModelForm):
    class Meta:
        model = CommentNonprofit
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

        labels = {
            'text': 'Your comment',
        }


class CommentVolunteerForm(forms.ModelForm):
    class Meta:
        model = CommentVolunteer
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

        labels = {
            'text': 'Your comment',
        }


class FundraisingCampaignForm(forms.ModelForm):
    class Meta:
        model = FundraisingCampaign
        fields = ('title', 'goal', 'description')

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'goal': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
        }

        labels = {
            'title': 'Title',
            'goal': 'Goal',
            'description': 'Description',
        }


class VolunteerVacancyForm(forms.ModelForm):
    class Meta:
        model = VolunteerVacancy
        fields = ('title', 'description')

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
        }

        labels = {
            'title': 'Title',
            'description': 'Description',
        }


class NonprofitEventForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = NonprofitEvent
        fields = ('title', 'description', 'date', 'location')

        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5}
            ),
            'date': forms.DateTimeInput(
                attrs={'type': 'date'}
            ),
            'location': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

        labels = {
            'title': 'Title',
            'description': 'Description',
            'date': 'Date',
            'location': 'Location',
        }


class DonationForm(forms.ModelForm):
    fund = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_fund=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Donation
        fields = ('fund', 'amount',)
