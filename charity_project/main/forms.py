from django import forms
from .models import (
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
    CommentFund,
    CommentNonprofit,
    CommentVolunteer,
    CustomUser,
    Donation
)


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
