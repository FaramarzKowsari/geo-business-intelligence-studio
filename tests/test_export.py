import csv
import io

from app.exporters import businesses_to_csv
from app.models import Business


def test_csv_export() -> None:
    csv_text = businesses_to_csv(
        [Business(id="1", name="A, B", category="cafe", source="sample")]
    )
    rows = list(csv.DictReader(io.StringIO(csv_text)))
    assert rows[0]["name"] == "A, B"
    assert rows[0]["source"] == "sample"
