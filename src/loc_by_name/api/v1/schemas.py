from typing import Self
from ninja import Schema

from loc_by_name.logic.models import Country


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
    def from_model(cls, model: Country) -> Self:
        return cls(
            probability=model.probability,
            country_name=model.country,
            region=model.region,
            independent=model.independent,
            capital_coords=(model.capital_longitude, model.capital_latitude),
            borders_with=model.borders_with,
            capital_name=model.capital_name,
            coat_of_arms_png=model.coat_of_arms_png,
            coat_of_arms_svg=model.coat_of_arms_svg,
            flag_alt=model.flag_alt,
            flag_png=model.flag_png,
            flag_svg=model.flag_svg,
            google_maps=model.google_maps,
            open_street_maps=model.open_street_maps,
        )


class NameFrequencyResponseSchema(Schema):
    times_appeared: int
    name: str
