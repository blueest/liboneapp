# Generated by Django 5.1.2 on 2024-10-24 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_onlinebook_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlinebook',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='online_books/'),
        ),
    ]
