from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import jsonfield


class Property(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    address = models.CharField(max_length=200)
    area = models.FloatField()
    rooms = models.IntegerField()
    floor = models.IntegerField()
    type = models.CharField(max_length=50)
    publication_date = models.DateField()
    images = models.TextField()
    realtor_id = models.IntegerField()

    def __str__(self):
        return self.title
    
    

class Application(models.Model):
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    application_date = models.DateField()
    status = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return self.applicant.username



class MarketAnalysis(models.Model):
    creationDate = models.DateField()
    analysis_properties = jsonfield.JSONField()
    analysis_results = jsonfield.JSONField()

    def __str__(self):
        return self.creationDate