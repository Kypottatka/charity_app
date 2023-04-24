# Generated by Django 4.1.7 on 2023-04-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_customuser_balance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='balance',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='balance',
            field=models.IntegerField(default=0, help_text='Balance'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_fund',
            field=models.BooleanField(default=False, help_text='Fund'),
        ),
    ]
