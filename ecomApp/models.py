from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class ExecutiveUser(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    zip = models.CharField(max_length=200, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    userPassword = models.CharField(max_length=200, blank=True, null=True)
    target = models.FloatField(default=0.0)
    user_ID = models.ForeignKey(User, blank=True, null=True)
    isDeleted = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'a) Sales Executive User List'

