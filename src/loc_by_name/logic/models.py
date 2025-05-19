from django.db import models
from django.contrib.postgres.fields import ArrayField


class Country(models.Model):
    name = models.CharField(max_length=100)
    count_of_requests = models.IntegerField(null=False, default=1)
    country = ArrayField(models.CharField(max_length=100), null=False)
    region = ArrayField(models.CharField(max_length=100), null=False)
    last_accessed = models.DateTimeField(null=True)
    independent = models.BooleanField(null=True)
    google_maps = models.URLField(null=True)
    open_street_map = models.URLField(null=True)
    probability = models.FloatField()
    capital_name = models.CharField(max_length=100)
    capital_latitude = models.FloatField()
    captial_longitude = models.FloatField()
    flag_png = models.URLField(null=True)
    flag_svg = models.URLField(null=True)
    flag_alt = models.CharField(null=True, max_length=200)
    coat_of_arms_png = models.URLField(null=True)
    coat_of_arms_svg = models.URLField(null=True)
    borders_with = ArrayField(models.CharField(max_length=100), null=True)
