from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Venue(models.Model):
    name = models.CharField('Venue name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField("Zip Code", max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Owner', blank=True, null=True)

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email Address')

    def __str__(self):
        return self.first_name + " " + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    # venue = models.CharField(max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name
