import httpx
import pytest

from location_finder.logic.services.external import ExternalCountryService


@pytest.mark.asyncio
async def test_web_country_service():
    async with httpx.AsyncClient() as client:
        service = ExternalCountryService(client)
        countries_by_name = await service.get_countries_by_person_name(
            person_name="Solovei"
        )

        assert len(countries_by_name) > 0

        country = await service.get_country_info_by_code(country_code="UA")
        assert country.independent is True
