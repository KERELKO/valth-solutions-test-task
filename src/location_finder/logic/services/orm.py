from datetime import datetime

from django.db.models import Q

from location_finder.core.exceptions import ServiceException
from location_finder.logic.dto import NameFrequencyDTO

from ..models import Country


class ORMCountryService:
    async def get_countries(
        self,
        country_name: str | None = None,
        person_name: str | None = None,
        last_accessed_date: datetime | None = None,
        limit: int = 10,
    ) -> list[Country]:
        q = Q()
        if country_name is not None:
            q &= Q(country__contains=[country_name])

        if person_name is not None:
            q &= Q(name=person_name.lower())

        if last_accessed_date is not None:
            q &= Q(last_accessed__gte=last_accessed_date)

        countries = Country.objects.filter(q)[:limit]
        return [c async for c in countries]

    async def store_country(
        self, name: str, probability: float, country_data: dict
    ) -> Country:
        country = Country(
            **country_data,
            name=name.lower(),
            probability=probability,
            count_of_requests=1,
            last_accessed=datetime.now(),
        )
        await country.asave()
        return country

    async def update_country_by_id(
        self,
        country_id: int,
        count_of_requests: int | None = None,
        last_accessed_date: datetime | None = None,
    ) -> Country:
        try:
            country = await Country.objects.aget(pk=country_id)
        except Country.DoesNotExist:
            raise ServiceException(msg=f'Country with ID "{country_id}" does not exist')
        if count_of_requests is not None:
            country.count_of_requests = count_of_requests
        if last_accessed_date is not None:
            country.last_accessed_date = last_accessed_date
        await country.asave()
        return country

    async def get_the_most_frequent_names(
        self,
        country_code: str,
        limit: int = 5,
    ) -> list[NameFrequencyDTO]:
        """Return the most frequent names by country code"""
        countries = Country.objects.filter(
            country__contains=country_code,
        ).order_by("-count_of_requests")[:limit]
        return [
            NameFrequencyDTO(count=c.count_of_requests, name=c.name)
            async for c in countries
        ]
