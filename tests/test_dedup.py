from app.models import Business
from app.services import deduplicate_businesses, quality_score


def business(identifier: str, name: str, address: str, phone: str = "") -> Business:
    return Business(
        id=identifier,
        name=name,
        address=address,
        phone=phone,
        source="test",
    )


def test_duplicate_phone_is_removed() -> None:
    items = [
        business("1", "Canal Coffee", "First Street", "+31 20 123 4567"),
        business("2", "Canal Coffee Amsterdam", "First Street 1", "+31 20 123 4567"),
    ]
    unique, removed = deduplicate_businesses(items)
    assert len(unique) == 1
    assert removed == 1


def test_distinct_businesses_are_kept() -> None:
    items = [
        business("1", "Canal Coffee", "First Street"),
        business("2", "Harbor Bakery", "Second Street"),
    ]
    unique, removed = deduplicate_businesses(items)
    assert len(unique) == 2
    assert removed == 0


def test_quality_score_rewards_complete_records() -> None:
    sparse = business("1", "Name", "")
    complete = Business(
        id="2",
        name="Name",
        category="cafe",
        address="Street",
        phone="123",
        website="https://example.com",
        email="a@example.com",
        latitude=1,
        longitude=2,
        rating=4.5,
        source="test",
    )
    assert quality_score(complete) > quality_score(sparse)
