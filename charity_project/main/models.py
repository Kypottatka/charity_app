from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser


# Кастомный пользователь - дает возможность
# дополнительно создавать аккаунты для фондов
# через полей is_fund
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    is_fund = models.BooleanField(default=False, help_text='Fund')


# Модель профиля для пользователей
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/')
    location = models.CharField(max_length=255, blank=True)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Balance'
    )


# Модель профиля для фондов
class FundProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='funds_avatars/')
    description = models.TextField(blank=True)
    raised = models.DecimalField(default=0, max_digits=20, decimal_places=2)


# Модель для донатов
# Пометка: позже добавить возможность привязки карты
# и сделать донаты через Stripe
class Donation(models.Model):
    user = models.ForeignKey(
        CustomUser,
        # related_name для обратной связи, предотвращает конфликты
        # полей user и fund
        related_name='user_donations',
        on_delete=models.CASCADE
    )
    fund = models.ForeignKey(
        CustomUser,
        related_name='fund_donations',
        on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


# Модели трех видов постов:
# 1. кампаний по сбору средств
class FundraisingCampaign(models.Model):
    fund = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    goal = models.TextField()
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('fundraising_campaign', kwargs={'pk': self.pk})


# 2. вакансий волонтеров
class VolunteerVacancy(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('volunteer_vacancy', kwargs={'pk': self.pk})


# 3. событий некоммерческих организаций
class NonprofitEvent(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('nonprofit_event', kwargs={'pk': self.pk})


# Модель для комментариев
class CommentFund(models.Model):
    post = models.ForeignKey(FundraisingCampaign, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CommentNonprofit(models.Model):
    post = models.ForeignKey(NonprofitEvent, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class CommentVolunteer(models.Model):
    post = models.ForeignKey(VolunteerVacancy, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
