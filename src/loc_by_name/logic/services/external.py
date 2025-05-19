from pprint import pprint
import httpx

from loc_by_name.core.exceptions import ServiceException
from loc_by_name.logic.dto import CountryInfoDTO


class ExternalCountryService:
    _base_nationalize_url: str = "https://api.nationalize.io"
    _base_rest_countries_url: str = "https://restcountries.com/v3.1"

    async def get_countries_by_person_name(
        self,
        person_name: str,
        client: httpx.AsyncClient,
    ) -> list[dict]:
        """Returns list where each element is a dict containing:
        * `country_id`: str (country code e.g. US)
        * `probability`: float (e.g. 0.114)
        """
        response = await client.get(f"{self._base_nationalize_url}?name={person_name}")
        if response.is_success is False:
            raise ServiceException(msg=f"Invalid country name: name={person_name}")
        data = response.json()
        return data["country"]

    async def get_country_info_by_code(
        self,
        country_code: str,
        client: httpx.AsyncClient,
    ) -> CountryInfoDTO:
        response = await client.get(
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
