from pprint import pprint
import httpx
import pytest

from loc_by_name.logic.services.external import ExternalCountryService


@pytest.mark.asyncio
async def test_web_country_service():
    service = ExternalCountryService()

    async with httpx.AsyncClient() as client:
        data = await service.get_countries_by_person_name(
            person_name="Solovei", client=client
        )
        print(data)

        data = await service.get_country_info_by_code(country_code="UA", client=client)
        pprint(data)
