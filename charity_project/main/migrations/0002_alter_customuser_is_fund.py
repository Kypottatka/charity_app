# Generated by Django 4.1.7 on 2023-04-03 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='is_fund',
            field=models.BooleanField(default=False, help_text='Фонд'),
        ),
    ]
