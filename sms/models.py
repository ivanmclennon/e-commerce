from django.db import models

# Create your models here.


class SMSLog(models.Model):
    code = models.CharField(max_length=4)
    response = models.JSONField()
