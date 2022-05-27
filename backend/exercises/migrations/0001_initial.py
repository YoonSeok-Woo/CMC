# Generated by Django 3.2.12 on 2022-04-07 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SampleImage',
            fields=[
                ('sample_image_id', models.AutoField(primary_key=True, serialize=False)),
                ('sample_image_name', models.CharField(max_length=50)),
                ('sample_image_path', models.CharField(max_length=255)),
                ('sample_image_data', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='SampleVideo',
            fields=[
                ('sample_video_id', models.AutoField(primary_key=True, serialize=False)),
                ('sample_video_name', models.CharField(max_length=50)),
                ('sample_video_path', models.CharField(max_length=255)),
                ('sample_video_data', models.TextField()),
            ],
        ),
    ]