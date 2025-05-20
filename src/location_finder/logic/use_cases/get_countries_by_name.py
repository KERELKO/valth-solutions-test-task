import asyncio
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from location_finder.logic.models import Country
from location_finder.logic.services.interfaces import CountryGetter, CountryStorage

from ..dto import CountryInfoDTO


@dataclass(eq=False, slots=True)
class CollectedCountryInfo:
    country: CountryInfoDTO
    probability: float
    name: str
    count_of_requests: int
    last_accessed_date: datetime


def _collect_country_info(country: Country) -> CollectedCountryInfo:
    result = CollectedCountryInfo(
        **country.get_metrics_data(),
        country=CountryInfoDTO(**country.get_country_data()),
    )
    return result


class GetCountriesByNameUseCase:
    def __init__(self, country_storage: CountryStorage, country_getter: CountryGetter):
        self.country_storage = country_storage
        self.country_getter = country_getter

    async def __call__(self, name: str):
        # Find countries that already exist in storage and have fresh data
        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
        countries = await self.country_storage.get_countries(
            person_name=name.lower(),
            last_accessed_date=one_day_ago,
        )

        # If countries with fresh data were found
        if len(countries) > 0:
            # Update their count of requests (Can be optimized with batch update)
            updated_countries = await asyncio.gather(
                *[
                    self.country_storage.update_country_by_id(
                        c.id,  # type: ignore
                        count_of_requests=c.count_of_requests + 1,
                    )
                    for c in countries
                ]
            )

            return [_collect_country_info(c) for c in updated_countries]

        # If countries with fresh data weren't found
        result: list[CollectedCountryInfo] = []
        # Get countries by name from external resources
        ex_countries = await self.country_getter.get_countries_by_person_name(
            person_name=name.lower(),
        )
        for ex_country in ex_countries:
            # For each country check if country data already exists in storage
            _stored_countries = await self.country_storage.get_countries(
                country_name=ex_country.country_code,
                limit=1,
            )
            stored_country = (
                _stored_countries[0] if len(_stored_countries) > 0 else None
            )

            # If country already exists in storage: store country data with new name and probability
            if stored_country:
                new_country_info = await self.country_storage.store_country(
                    probability=ex_country.probability,
                    name=name,
                    country_data=stored_country.asdict(remove_non_country_fields=True),
                )
                result.append(_collect_country_info(new_country_info))
                continue

            # If country does not exist in storage:
            # make request to external resources for country data by country code
            country_info = await self.country_getter.get_country_info_by_code(
                ex_country.country_code,
            )
            country_info_dict = asdict(country_info)
            country_info_dict["country"] = country_info_dict.pop("name")

            capital_coords: tuple[float, float] = country_info_dict.pop(
                "capital_coords"
            )
            country_info_dict["capital_longitude"] = capital_coords[0]
            country_info_dict["capital_latitude"] = capital_coords[1]

            # Store new country with new name and probability
            saved_country = await self.country_storage.store_country(
                country_data=country_info_dict,
                probability=ex_country.probability,
                name=name,
            )
            result.append(_collect_country_info(saved_country))
        return result
