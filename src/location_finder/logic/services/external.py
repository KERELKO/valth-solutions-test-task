from pprint import pprint
import httpx

from location_finder.core.exceptions import ServiceException
from location_finder.logic.dto import CountryInfoDTO, CountryProbabilityForNameDTO


class ExternalCountryService:
    _base_nationalize_url: str = "https://api.nationalize.io"
    _base_rest_countries_url: str = "https://restcountries.com/v3.1"

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def get_countries_by_person_name(
        self,
        person_name: str,
    ) -> list[CountryProbabilityForNameDTO]:
        """Returns list with countries probabilities by person name"""
        response = await self.client.get(
            f"{self._base_nationalize_url}?name={person_name}"
        )
        if response.is_success is False:
            raise ServiceException(msg=f"Invalid country name: name={person_name}")
        data = response.json()
        return [
            CountryProbabilityForNameDTO(
                country_code=c["country_id"], probability=c["probability"]
            )
            for c in data["country"]
        ]

    async def get_country_info_by_code(self, country_code: str) -> CountryInfoDTO:
        response = await self.client.get(
            f"{self._base_rest_countries_url}/alpha/{country_code}"
        )
        if response.is_success is False:
            raise ServiceException(msg=f"Invalid country code: code={country_code}")
        data = response.json()[0]

        pprint(data)
        capital = data.get("capital", None)
        if capital is not None:
            capital = capital[0]

        name = data.get("name")
        country_name = name.get("official", None) or name.get("common")

        capital_info = data.get("capitalInfo", None)
        if capital_info is None:
            capital_coords = None
        else:
            latlng = capital_info["latlng"]
            capital_coords = (latlng[0], latlng[1])

        return CountryInfoDTO(
            borders_with=data.get("borders", None),
            capital_name=capital,
            capital_coords=capital_coords,
            name=[country_code, country_name],
            region=[data["region"]],
            independent=data["independent"],
            google_maps=data.get("maps", {}).get("googleMaps", None),
            open_street_maps=data.get("maps", {}).get("openStreetMaps", None),
            flag_alt=data.get("flags", {}).get("alt", None),
            flag_png=data.get("flags", {}).get("png", None),
            flag_svg=data.get("flags", {}).get("svg", None),
            coat_of_arms_png=data.get("coatOfArms", {}).get("png", None),
            coat_of_arms_svg=data.get("coatOfArms", {}).get("svg", None),
        )
