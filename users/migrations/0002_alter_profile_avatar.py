# Generated by Django 4.2.2 on 2023-08-06 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='uploads/profiles/default.jpg', null=True, upload_to='uploads/profiles/%Y/%m/'),
        ),
    ]