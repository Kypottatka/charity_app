# Generated by Django 4.1.7 on 2023-04-23 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_alter_userprofile_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='fundprofile',
            name='raised',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=20),
        ),
    ]
