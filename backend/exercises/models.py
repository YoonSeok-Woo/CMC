from operator import mod
from django.db import models

# Create your models here.
class SampleImage(models.Model):
    sample_image_id = models.AutoField(primary_key=True)
    sample_image_name = models.CharField(max_length=50)
    sample_image_path = models.CharField(max_length=255)
    sample_image_data = models.TextField()


class SampleVideo(models.Model):
    sample_video_id = models.AutoField(primary_key=True)
    sample_video_name = models.CharField(max_length=50)
    sample_video_path = models.CharField(max_length=255)
    sample_video_data = models.TextField()