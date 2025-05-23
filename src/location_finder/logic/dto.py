from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, eq=False)
class CountryInfoDTO:
    name: list[str]
    independent: bool
    region: list[str]
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


@dataclass(slots=True, eq=False)
class NameFrequencyDTO:
    count: int
    name: str


@dataclass(slots=True, eq=False)
class CountryProbabilityForNameDTO:
    probability: float
    country_code: str


@dataclass(slots=True, eq=False)
class MetricsDTO:
    count_of_requests: int
    name: str
    last_accessed_date: datetime
    probability: float
