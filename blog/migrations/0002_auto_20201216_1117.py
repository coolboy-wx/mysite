# Generated by Django 3.1.4 on 2020-12-16 03:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogarticles',
            name='publish',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='发布时间'),
        ),
    ]
