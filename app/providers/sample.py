import json
from pathlib import Path

from app.models import Business, SearchRequest
from app.providers.base import BusinessProvider


class SampleProvider(BusinessProvider):
    id = "sample"
    label = "Sample data"

    def __init__(self) -> None:
        path = Path(__file__).resolve().parent.parent / "data" / "sample_businesses.json"
        self._records = [
            Business.model_validate(item) for item in json.loads(path.read_text("utf-8"))
        ]

    async def search(self, request: SearchRequest) -> list[Business]:
        query_tokens = {token.casefold() for token in request.query.split() if token}
        city = request.city.casefold()

        def matches(record: Business) -> bool:
            haystack = f"{record.name} {record.category} {record.address}".casefold()
            city_match = city in record.city.casefold() or record.city.casefold() in city
            query_match = any(token in haystack for token in query_tokens)
            return city_match and query_match

        results = [record.model_copy(deep=True) for record in self._records if matches(record)]
        if not results:
            city_results = [
                record.model_copy(deep=True)
                for record in self._records
                if city in record.city.casefold() or record.city.casefold() in city
            ]
            results = city_results or [record.model_copy(deep=True) for record in self._records]
        return results[: request.limit]
