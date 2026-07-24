import httpx

from app.config import Settings
from app.models import Business, SearchRequest
from app.providers.base import BusinessProvider, ProviderError


class GooglePlacesProvider(BusinessProvider):
    id = "google_places"
    label = "Google Places API (official)"
    endpoint = "https://places.googleapis.com/v1/places:searchText"

    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def search(self, request: SearchRequest) -> list[Business]:
        if not self.settings.google_places_api_key:
            raise ProviderError(
                "Google Places is not configured. Add GOOGLE_PLACES_API_KEY "
                "to your local .env file."
            )

        fields = (
            "places.id,places.displayName,places.formattedAddress,places.location,"
            "places.primaryType,places.rating,places.userRatingCount,"
            "places.internationalPhoneNumber,places.websiteUri,places.googleMapsUri"
        )
        headers = {
            "Content-Type": "application/json",
            "X-Goog-Api-Key": self.settings.google_places_api_key,
            "X-Goog-FieldMask": fields,
        }
        body = {
            "textQuery": f"{request.query} in {request.city}",
            "pageSize": min(request.limit, 20),
            "languageCode": request.language,
        }
        async with httpx.AsyncClient(timeout=self.settings.request_timeout_seconds) as client:
            response = await client.post(self.endpoint, json=body, headers=headers)
        if response.status_code in {401, 403}:
            raise ProviderError("Google Places rejected the API key or project configuration.")
        if response.status_code == 429:
            raise ProviderError("Google Places quota or rate limit reached.")
        response.raise_for_status()

        businesses: list[Business] = []
        for place in response.json().get("places", []):
            location = place.get("location", {})
            display_name = place.get("displayName", {})
            businesses.append(
                Business(
                    id=f"google-{place.get('id', len(businesses))}",
                    name=display_name.get("text", "Unnamed place"),
                    category=(place.get("primaryType") or "business").replace("_", " "),
                    address=place.get("formattedAddress", ""),
                    city=request.city,
                    phone=place.get("internationalPhoneNumber", ""),
                    website=place.get("websiteUri", ""),
                    latitude=location.get("latitude"),
                    longitude=location.get("longitude"),
                    rating=place.get("rating"),
                    review_count=place.get("userRatingCount"),
                    source="google_places",
                    source_url=place.get("googleMapsUri", ""),
                )
            )
        return businesses[: request.limit]
