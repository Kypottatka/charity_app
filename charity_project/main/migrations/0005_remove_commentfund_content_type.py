# Generated by Django 4.1.7 on 2023-04-05 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_commentfund_delete_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentfund',
            name='content_type',
        ),
    ]
