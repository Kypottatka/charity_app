# Generated by Django 4.1.7 on 2023-04-23 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_donation_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='balance',
            field=models.IntegerField(default=0, help_text='Баланс'),
        ),
    ]