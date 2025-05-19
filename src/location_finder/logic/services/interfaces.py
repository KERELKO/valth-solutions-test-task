from datetime import datetime
from typing import Protocol

from location_finder.logic.dto import (
    CountryInfoDTO,
    CountryProbabilityForNameDTO,
    NameFrequencyDTO,
)
from location_finder.logic.models import Country


class CountryGetter(Protocol):
    async def get_countries_by_person_name(
        self,
        person_name: str,
    ) -> list[CountryProbabilityForNameDTO]:
        raise NotImplementedError

    async def get_country_info_by_code(self, country_code: str) -> CountryInfoDTO:
        raise NotImplementedError


class CountryStorage(Protocol):
    async def get_countries(
        self,
        country_name: str | None = None,
        person_name: str | None = None,
        last_accessed_date: datetime | None = None,
        limit: int = 10,
    ) -> list[Country]:
        raise NotImplementedError

    async def store_country(
        self, name: str, probability: float, country_data: dict
    ) -> Country:
        raise NotImplementedError

    async def update_country_by_id(
        self,
        country_id: int,
        count_of_requests: int | None = None,
        last_accessed_date: datetime | None = None,
    ) -> Country:
        raise NotImplementedError

    async def get_the_most_frequent_names(
        self,
        country_code: str,
        limit: int = 5,
    ) -> list[NameFrequencyDTO]:
        raise NotImplementedError
