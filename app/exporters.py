import csv
import io

from app.models import Business

EXPORT_FIELDS = [
    "name",
    "category",
    "address",
    "city",
    "country",
    "phone",
    "website",
    "email",
    "latitude",
    "longitude",
    "rating",
    "review_count",
    "quality_score",
    "source",
    "source_url",
]


def businesses_to_csv(businesses: list[Business]) -> str:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=EXPORT_FIELDS, extrasaction="ignore")
    writer.writeheader()
    for business in businesses:
        writer.writerow(business.model_dump(include=set(EXPORT_FIELDS)))
    return buffer.getvalue()
