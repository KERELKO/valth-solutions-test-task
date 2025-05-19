import asyncio
from dataclasses import asdict
from datetime import timedelta

import httpx

from ninja import Router
from django.http.response import HttpResponseNotFound
from django.http import HttpRequest
from django.utils import timezone

from loc_by_name.logic.services.external import ExternalCountryService
from loc_by_name.logic.services.orm import ORMCountryService

from .schemas import CountryInfoResponseSchema, NameFrequencyResponseSchema


router = Router()


@router.get("/names")
async def get_info_by_name_handler(
    request: HttpRequest,
    name: str,
) -> list[CountryInfoResponseSchema] | HttpResponseNotFound:
    external_country_service = ExternalCountryService()
    orm_country_sevice = ORMCountryService()
    one_day_ago = timezone.now() - timedelta(days=1)

    countries = await orm_country_sevice.get_countries(
        person_name=name.lower(),
        last_accessed_date=one_day_ago,
    )

    if len(countries) > 0:
        updated_countries = await asyncio.gather(
            *[
                orm_country_sevice.update_country_by_id(
                    c.id,
                    count_of_requests=c.count_of_requests + 1,  # type: ignore
                )
                for c in countries
            ]
        )
        return [CountryInfoResponseSchema.from_model(c) for c in updated_countries]

    result: list[CountryInfoResponseSchema] = []
    async with httpx.AsyncClient() as client:
        ex_countries = await external_country_service.get_countries_by_person_name(
            person_name=name.lower(),
            client=client,
        )
        for ex_country in ex_countries:
            country_code = ex_country["country_id"]
            probability = ex_country["probability"]
            _stored_countries = await orm_country_sevice.get_countries(
                country_name=country_code,
                limit=1,
            )
            stored_country = (
                _stored_countries[0] if len(_stored_countries) > 0 else None
            )

            if stored_country:
                stored_country_data = stored_country.asdict()
                stored_country_data.pop("probability")
                stored_country_data.pop("name")
                stored_country_data.pop("count_of_requests")
                stored_country_data.pop("last_accessed")

                new_country_info = await orm_country_sevice.store_country(
                    probability=probability,
                    name=name,
                    country_data=stored_country_data,
                )
                result.append(CountryInfoResponseSchema.from_model(new_country_info))
                continue

            country_info = await external_country_service.get_country_info_by_code(
                country_code,
                client,
            )
            country_info_dict = asdict(country_info)
            country_info_dict["country"] = country_info_dict.pop("name")

            capital_coords: tuple[float, float] = country_info_dict.pop(
                "capital_coords"
            )
            country_info_dict["capital_longitude"] = capital_coords[0]
            country_info_dict["capital_latitude"] = capital_coords[1]

            saved_country = await orm_country_sevice.store_country(
                country_data=country_info_dict,
                probability=probability,
                name=name,
            )
            result.append(CountryInfoResponseSchema.from_model(saved_country))

    if not result:
        return HttpResponseNotFound()

    return result


@router.get("/popular-names")
async def get_popular_names(
    request: HttpRequest,
    country_code: str,
) -> list[NameFrequencyResponseSchema] | HttpResponseNotFound:
    orm_country_service = ORMCountryService()
    result = await orm_country_service.get_the_most_frequent_names(country_code, 5)

    if len(result) == 0:
        return HttpResponseNotFound(content=f"No names by {country_code}")

    return [
        NameFrequencyResponseSchema(times_appeared=d.count, name=d.name) for d in result
    ]
