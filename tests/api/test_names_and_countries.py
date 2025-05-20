import httpx
import pytest

POPULAR_NAMES_ENDPOINT = "http://localhost:8000/api/popular-names"
COUNTRY_PROBABILITY_ENDPOINT = "http://localhost:8000/api/names"


class TestPopularNamesAndCountriesEndpoints:
    @pytest.mark.asyncio
    async def test_can_get_country_probability_by_name(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                COUNTRY_PROBABILITY_ENDPOINT, params={"name": "solovei"}
            )
            assert response.is_success
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            for country in data:
                assert "probability" in country
                assert "country_name" in country

    @pytest.mark.asyncio
    async def test_popular_names(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                POPULAR_NAMES_ENDPOINT, params={"country_code": "UA"}
            )
            assert response.is_success
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            for d in data:
                assert "times_appeared" in d
                assert "name" in d


@pytest.mark.asyncio
async def test_cannot_make_request_to_popular_names_endpoint():
    async with httpx.AsyncClient() as client:
        response_400 = await client.get(POPULAR_NAMES_ENDPOINT)
        assert response_400.status_code == 400

        response_404 = await client.get(
            POPULAR_NAMES_ENDPOINT, params={"country_code": "JMFDLSKF"}
        )
        assert response_404.status_code == 404


@pytest.mark.asyncio
async def test_cannot_make_request_to_country_probability_endpoint():
    async with httpx.AsyncClient() as client:
        response_400 = await client.get(COUNTRY_PROBABILITY_ENDPOINT)
        assert response_400.status_code == 400

        response_404 = await client.get(
            COUNTRY_PROBABILITY_ENDPOINT,
            params={"name": "TESTDOESNOTEXIST"},
        )
        assert response_404.status_code == 404
