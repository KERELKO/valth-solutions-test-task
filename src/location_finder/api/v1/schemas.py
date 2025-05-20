from typing import Self
from ninja import Schema

from location_finder.logic.use_cases.get_countries_by_name import CollectedCountryInfo


class CountryInfoResponseSchema(Schema):
    probability: float
    country_name: list[str]
    region: list[str]
    independent: bool | None = None
    capital_coords: tuple[float, float] | None = None
    borders_with: list[str] | None = None
    capital_name: str | None = None
    coat_of_arms_png: str | None = None
    coat_of_arms_svg: str | None = None
    flag_alt: str | None = None
    flag_png: str | None = None
    flag_svg: str | None = None
    google_maps: str | None = None
    open_street_maps: str | None = None

    @classmethod
    def from_collected_country_info(cls, info: CollectedCountryInfo) -> Self:
        result = cls(
            probability=info.probability,
            country_name=info.country.name,
            region=info.country.region,
            independent=info.country.independent,
            capital_coords=(
                info.country.capital_coords[0],  # type: ignore
                info.country.capital_coords[1],  # type: ignore
            ),
            borders_with=info.country.borders_with,
            capital_name=info.country.capital_name,
            coat_of_arms_png=info.country.coat_of_arms_png,
            coat_of_arms_svg=info.country.coat_of_arms_svg,
            flag_alt=info.country.flag_alt,
            flag_png=info.country.flag_png,
            flag_svg=info.country.flag_svg,
            google_maps=info.country.google_maps,
            open_street_maps=info.country.open_street_maps,
        )
        return result


class NameFrequencyResponseSchema(Schema):
    times_appeared: int
    name: str
