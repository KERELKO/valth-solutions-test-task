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
    last_acccessed_date: datetime


def _collect_country_info(country: Country) -> CollectedCountryInfo:
    return CollectedCountryInfo(
        country=CountryInfoDTO(**country.get_country_data()),
        **country.get_metrics_data(),
    )


class GetCountriesByNameUseCase:
    def __init__(self, country_storage: CountryStorage, country_getter: CountryGetter):
        self.country_storage = country_storage
        self.country_getter = country_getter

    async def __call__(self, name: str):
        one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)

        countries = await self.country_storage.get_countries(
            person_name=name.lower(),
            last_accessed_date=one_day_ago,
        )

        if len(countries) > 0:
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

        result: list[CollectedCountryInfo] = []
        ex_countries = await self.country_getter.get_countries_by_person_name(
            person_name=name.lower(),
        )
        for ex_country in ex_countries:
            _stored_countries = await self.country_storage.get_countries(
                country_name=ex_country.country_code,
                limit=1,
            )
            stored_country = (
                _stored_countries[0] if len(_stored_countries) > 0 else None
            )

            if stored_country:
                new_country_info = await self.country_storage.store_country(
                    probability=ex_country.probability,
                    name=name,
                    country_data=stored_country.asdict(),
                )
                result.append(_collect_country_info(new_country_info))
                continue

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

            saved_country = await self.country_storage.store_country(
                country_data=country_info_dict,
                probability=ex_country.probability,
                name=name,
            )
            result.append(_collect_country_info(saved_country))
        return result
