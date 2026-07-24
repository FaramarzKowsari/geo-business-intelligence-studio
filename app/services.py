import re
import unicodedata
from difflib import SequenceMatcher

from app.models import Business, SearchMeta, SearchRequest, SearchResponse
from app.providers.base import BusinessProvider


def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(char for char in value if not unicodedata.combining(char))
    value = value.casefold()
    return re.sub(r"[^\w]+", "", value, flags=re.UNICODE)


def quality_score(business: Business) -> int:
    score = 20 if business.name else 0
    score += 15 if business.category else 0
    score += 15 if business.address else 0
    score += 15 if business.phone else 0
    score += 15 if business.website else 0
    score += 10 if business.email else 0
    score += 5 if business.latitude is not None and business.longitude is not None else 0
    score += 5 if business.rating is not None else 0
    return min(score, 100)


def is_duplicate(left: Business, right: Business) -> bool:
    left_phone = normalize_text(left.phone)
    right_phone = normalize_text(right.phone)
    if left_phone and right_phone and left_phone == right_phone:
        return True

    left_name = normalize_text(left.name)
    right_name = normalize_text(right.name)
    if not left_name or not right_name:
        return False
    name_similarity = SequenceMatcher(None, left_name, right_name).ratio()

    left_address = normalize_text(left.address)
    right_address = normalize_text(right.address)
    address_similarity = (
        SequenceMatcher(None, left_address, right_address).ratio()
        if left_address and right_address
        else 0.0
    )
    return name_similarity >= 0.94 or (name_similarity >= 0.84 and address_similarity >= 0.72)


def deduplicate_businesses(items: list[Business]) -> tuple[list[Business], int]:
    unique: list[Business] = []
    removed = 0
    for item in items:
        if any(is_duplicate(item, existing) for existing in unique):
            removed += 1
            continue
        unique.append(item)
    return unique, removed


class SearchService:
    def __init__(self, providers: dict[str, BusinessProvider]) -> None:
        self.providers = providers

    async def search(self, request: SearchRequest) -> SearchResponse:
        provider = self.providers[request.provider.value]
        businesses = await provider.search(request)
        for business in businesses:
            business.quality_score = quality_score(business)
        businesses.sort(key=lambda item: (item.quality_score, item.rating or 0), reverse=True)

        removed = 0
        if request.deduplicate:
            businesses, removed = deduplicate_businesses(businesses)

        warnings: list[str] = []
        if request.provider.value == "openstreetmap":
            warnings.append(
                "OpenStreetMap coverage varies by region. Verify contact fields before use."
            )
        if request.provider.value == "sample":
            warnings.append("Sample records are fictional and intended only for demonstration.")

        return SearchResponse(
            businesses=businesses[: request.limit],
            meta=SearchMeta(
                provider=request.provider.value,
                query=request.query,
                city=request.city,
                returned=min(len(businesses), request.limit),
                duplicates_removed=removed,
                warnings=warnings,
            ),
        )
