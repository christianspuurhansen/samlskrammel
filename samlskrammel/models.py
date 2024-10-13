from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Friend(models.Model):
  myOwner = models.ForeignKey(
    User,
    models.CASCADE,
    blank=False,
    null=False,
    related_name='owner'
  )
  myFriend = models.ForeignKey(
    User,
    models.CASCADE,
    blank=False,
    null=False,
    related_name='friend'
  )

class Post(models.Model):
  myWhat = models.CharField(max_length=255, help_text='Hvilket skrald er blevet samlet?')
  myWeight = models.DecimalField(max_digits=10, decimal_places=3)
  myWhereLat = models.DecimalField(max_digits=10, decimal_places=7)
  myWhereLon = models.DecimalField(max_digits=10, decimal_places=7)
  myWhen = models.DateTimeField(auto_now=True)
  myOwner = models.ForeignKey(
    User,
    models.SET_NULL,
    blank=True,
    null=True,
  )
  myImage = models.ImageField(
    upload_to='static/images/',
    null=True
  )
