from django.db import models

# Create your models here.
class Device(models.Model):
    #deviceID = models.AutoField(primary_key=True)
    deviceName = models.CharField(max_length=100)
    showName = models.CharField(max_length = 100, blank=True)
    visionAI = models.BooleanField(default=False)

    def __str__(self):
        return self.deviceName
