# Generated by Django 3.2.12 on 2022-04-07 16:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TodaySchedule',
            fields=[
                ('todayschedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('todayschedule_title', models.CharField(max_length=50)),
                ('todayschedule_time', models.DateTimeField()),
                ('todayschedule_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='today_schedule', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('schedule_title', models.CharField(max_length=50)),
                ('schedule_time', models.DateTimeField()),
                ('schedule_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='schedule', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
