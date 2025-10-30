from django.db import models

# Create your models here.
class MyUser(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    created_at = models.DateField(auto_now_add=True)
    external_data = models.JSONField(null=True, blank=True)