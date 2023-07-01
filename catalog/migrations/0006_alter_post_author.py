# Generated by Django 4.2.2 on 2023-07-01 20:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('catalog', '0005_alter_post_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(blank=True, default='Other', on_delete=django.db.models.deletion.SET_DEFAULT, to='users.profile'),
        ),
    ]
