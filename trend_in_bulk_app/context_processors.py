from __future__ import annotations

from typing import Any

from django.conf import settings


def _star_parts(rating: float) -> list[str]:
    rating = max(0.0, min(5.0, float(rating)))
    full = int(rating)
    remainder = rating - full
    half = 1 if 0.25 <= remainder < 0.75 else 0
    if remainder >= 0.75:
        full = min(5, full + 1)
    empty = max(0, 5 - full - half)
    return (["full"] * full) + (["half"] * half) + (["empty"] * empty)


from .models import ContactMessage


def google_reviews(request) -> dict[str, Any]:
    rating = getattr(settings, "GOOGLE_REVIEW_RATING", 0.0)
    count = getattr(settings, "GOOGLE_REVIEW_COUNT", 0)
    url = getattr(settings, "GOOGLE_REVIEW_URL", "")
    return {
        "google_review_rating": rating,
        "google_review_count": count,
        "google_review_url": url,
        "google_review_stars": _star_parts(rating),
    }


def admin_unread_contacts(request) -> dict[str, Any]:
    unread_contacts = 0
    if request.user.is_authenticated and request.user.is_staff:
        unread_contacts = ContactMessage.objects.filter(is_read=False).count()
    return {
        "admin_unread_contact_count": unread_contacts,
        "admin_unread_enquiries_total": unread_contacts
    }


from .models import Category


def menu_categories(request):
    return {"menu_categories": Category.objects.all()}
