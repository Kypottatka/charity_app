from django import forms
from .models import (
    FundraisingCampaign,
    VolunteerVacancy,
    NonprofitEvent,
    Comment,
    CustomUser,
)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3}
            ),
        }

        labels = {
            'text': 'Текст комментария',
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
            'title': 'Заголовок',
            'goal': 'Цель сбора',
            'description': 'Описание',
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
            'title': 'Заголовок',
            'description': 'Описание',
        }


class NonprofitEventForm(forms.ModelForm):
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
                attrs={'class': 'form-control'}
            ),
            'location': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
        }

        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'date': 'Дата',
            'location': 'Место проведения',
        }


class DonationForm(forms.Form):
    fund = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(is_fund=True),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        fields = ('fund', 'amount',)
