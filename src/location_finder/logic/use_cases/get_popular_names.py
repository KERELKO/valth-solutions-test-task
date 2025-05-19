from location_finder.logic.services.interfaces import CountryStorage

from ..dto import NameFrequencyDTO


class GetPopularNamesUseCase:
    def __init__(self, country_storage: CountryStorage):
        self.country_storage = country_storage

    async def __call__(self, country_code: str) -> list[NameFrequencyDTO] | None:
        names = await self.country_storage.get_the_most_frequent_names(
            country_code, limit=5
        )

        if not names:
            return None

        return names
