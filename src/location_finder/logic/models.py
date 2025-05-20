from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex

from django.forms.models import model_to_dict


class Country(models.Model):
    name = models.CharField(max_length=100)
    probability = models.FloatField()
    count_of_requests = models.IntegerField(null=False, default=1)
    last_accessed_date = models.DateTimeField(null=True)

    country = ArrayField(models.CharField(max_length=100), null=False)
    region = ArrayField(models.CharField(max_length=100), null=False)
    independent = models.BooleanField(null=True)
    google_maps = models.URLField(null=True)
    open_street_maps = models.URLField(null=True)
    capital_name = models.CharField(max_length=100)
    capital_latitude = models.FloatField()
    capital_longitude = models.FloatField()
    flag_png = models.URLField(null=True)
    flag_svg = models.URLField(null=True)
    flag_alt = models.TextField(null=True)
    coat_of_arms_png = models.URLField(null=True)
    coat_of_arms_svg = models.URLField(null=True)
    borders_with = ArrayField(models.CharField(max_length=100), null=True)

    class Meta:
        verbose_name_plural = "countries"
        indexes = [models.Index(fields=["name"]), GinIndex(fields=["country"])]
        app_label = "logic"

    def asdict(self, remove_non_country_fields: bool = False) -> dict:
        data = model_to_dict(self)

        if remove_non_country_fields:
            data.pop("id")
            data.pop("probability")
            data.pop("name")
            data.pop("count_of_requests")
            data.pop("last_accessed_date")

        return data

    def get_country_data(self) -> dict:
        data = self.asdict(remove_non_country_fields=True)
        data["name"] = data.pop("country")
        data["capital_coords"] = (
            data.pop("capital_latitude"),
            data.pop("capital_longitude"),
        )
        return data

    def get_metrics_data(self) -> dict:
        return {
            "name": self.name,
            "last_accessed_date": self.last_accessed_date,
            "probability": self.probability,
            "count_of_requests": self.count_of_requests,
        }

    def __str__(self) -> str:
        return f'{self.name.capitalize()} ({','.join(self.country)})'
