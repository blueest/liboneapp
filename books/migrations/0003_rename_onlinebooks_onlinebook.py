# Generated by Django 5.1.2 on 2024-10-23 23:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_onlinebooks'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OnlineBooks',
            new_name='OnlineBook',
        ),
    ]
