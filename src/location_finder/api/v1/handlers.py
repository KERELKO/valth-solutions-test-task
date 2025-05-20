import httpx

from ninja import Router
from django.http.response import HttpResponseNotFound
from django.http import HttpRequest

from location_finder.logic.services.external import ExternalCountryService
from location_finder.logic.services.orm import ORMCountryService
from location_finder.logic.use_cases.get_countries_by_name import (
    GetCountriesByNameUseCase,
)
from location_finder.logic.use_cases.get_popular_names import GetPopularNamesUseCase

from .schemas import CountryInfoResponseSchema, NameFrequencyResponseSchema


router = Router()
country_storage = ORMCountryService()


@router.get("/names", response=list[CountryInfoResponseSchema])
async def get_info_by_name_handler(
    request: HttpRequest,
    name: str,
) -> list[CountryInfoResponseSchema] | HttpResponseNotFound:
    async with httpx.AsyncClient() as client:
        get_countries = GetCountriesByNameUseCase(
            country_storage, ExternalCountryService(client)
        )
        result = await get_countries(name)

    if not result:
        return HttpResponseNotFound()

    return [CountryInfoResponseSchema.from_collected_country_info(d) for d in result]


@router.get("/popular-names", response=list[NameFrequencyResponseSchema])
async def get_popular_names(
    request: HttpRequest,
    country_code: str,
) -> list[NameFrequencyResponseSchema] | HttpResponseNotFound:
    get_popular_names = GetPopularNamesUseCase(country_storage=country_storage)

    names = await get_popular_names(country_code)

    if not names:
        return HttpResponseNotFound()

    return [
        NameFrequencyResponseSchema(times_appeared=d.count, name=d.name) for d in names
    ]
