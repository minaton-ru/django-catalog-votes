# Generated by Django 4.2.2 on 2023-07-01 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('catalog', '0003_alter_post_author'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, default='blank', on_delete=django.db.models.deletion.SET_DEFAULT, to='users.profile'),
        ),
    ]
