"""Caption copy in the established Field Notes voice: numbers first, short
declarative sentences, present tense, no exclamation points, no hype
adjectives. See brand/stroll-savor-ci-guide.html section 01 for the full
voice principles this follows.

Hashtag strategy is intentionally out of scope here -- it's a distribution
decision, not a brand-voice one, and hasn't been decided yet."""
from datetime import datetime


def month_label(travel_month: str) -> str:
    return datetime.strptime(travel_month, "%Y-%m").strftime("%B %Y")


def carousel_caption(data: dict, flat_picks: list) -> str:
    label = month_label(data["travel_month"])
    lines = [
        f"{label} Spontaneous Escapes, business class. {data.get('discount_pct', 30)}% off Saver Awards.",
        "",
        f"{len(data['deals'])} business-class fares on offer this cycle. {len(flat_picks)} picked here, ranked by miles per hour in the air, best three per region.",
        "",
    ]
    for deal, region in flat_picks:
        lines.append(f"{deal['route_label']} — {deal['miles']:,} mi")
    lines += [
        "",
        f"Book by {data['booking_window']['end']}. Travel {data['travel_window']['start']} to {data['travel_window']['end']}.",
        "Discounts may run one direction only — check both legs before booking.",
        "Full list and live availability: link in bio.",
    ]
    return "\n".join(lines)


def story_caption(deal: dict, data: dict) -> str:
    label = month_label(data["travel_month"])
    return (
        f"{deal['route_label']} — {deal['miles']:,} mi, business class.\n"
        f"{data.get('discount_pct', 30)}% off Saver Award, {label} Spontaneous Escapes. "
        f"Book by {data['booking_window']['end']}."
    )


def web_artifact_caption(data: dict) -> str:
    label = month_label(data["travel_month"])
    return (
        f"The full {label} Spontaneous Escapes list, business class only — "
        f"{len(data['deals'])} fares, straight from the source. Link in bio."
    )
