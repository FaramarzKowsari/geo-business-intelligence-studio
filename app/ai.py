import json

import httpx

from app.config import Settings
from app.models import AnalysisRequest, AnalysisResponse
from app.providers.base import ProviderError


def deterministic_analysis(request: AnalysisRequest) -> str:
    businesses = request.businesses
    total = len(businesses)
    with_phone = sum(bool(item.phone) for item in businesses)
    with_website = sum(bool(item.website) for item in businesses)
    with_email = sum(bool(item.email) for item in businesses)
    ratings = [item.rating for item in businesses if item.rating is not None]
    average_rating = sum(ratings) / len(ratings) if ratings else None
    categories: dict[str, int] = {}
    for item in businesses:
        categories[item.category or "uncategorized"] = categories.get(item.category or "uncategorized", 0) + 1
    leading_categories = sorted(categories.items(), key=lambda pair: pair[1], reverse=True)[:5]
    category_text = ", ".join(f"{name} ({count})" for name, count in leading_categories)
    rating_text = f"{average_rating:.2f}/5" if average_rating is not None else "not available"
    return (
        f"Dataset overview: {total} businesses. Phone coverage: {with_phone}/{total}; "
        f"website coverage: {with_website}/{total}; email coverage: {with_email}/{total}. "
        f"Average available rating: {rating_text}. Leading categories: {category_text or 'none'}. "
        "Recommended next step: verify records with low quality scores before outreach or analysis."
    )


class AIAnalyzer:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        provider = self.settings.ai_provider.casefold()
        if provider == "none":
            return AnalysisResponse(
                provider="deterministic",
                model="built-in",
                text=deterministic_analysis(request),
            )
        if provider not in {"ollama", "openai_compatible"}:
            raise ProviderError("AI_PROVIDER must be none, ollama, or openai_compatible.")

        compact = [
            item.model_dump(
                include={
                    "name",
                    "category",
                    "address",
                    "phone",
                    "website",
                    "email",
                    "rating",
                    "review_count",
                    "quality_score",
                }
            )
            for item in request.businesses
        ]
        system = (
            "You are a careful business-data analyst. Use only the supplied records. "
            "Separate observations from inferences, mention missing data, and do not invent facts."
        )
        user = f"Instruction: {request.instruction}\nRecords:\n{json.dumps(compact, ensure_ascii=False)}"
        headers = {"Content-Type": "application/json"}
        if self.settings.ai_api_key:
            headers["Authorization"] = f"Bearer {self.settings.ai_api_key}"
        payload = {
            "model": self.settings.ai_model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "temperature": 0.2,
        }
        endpoint = f"{self.settings.ai_base_url.rstrip('/')}/chat/completions"
        async with httpx.AsyncClient(timeout=90) as client:
            response = await client.post(endpoint, json=payload, headers=headers)
        if response.status_code in {401, 403}:
            raise ProviderError("The configured AI endpoint rejected its credentials.")
        response.raise_for_status()
        data = response.json()
        try:
            text = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("The AI endpoint returned an unexpected response format.") from exc
        return AnalysisResponse(provider=provider, model=self.settings.ai_model, text=text)
