"""Step 5 -- Package: generate YouTube-ready titles, descriptions, chapters, and tags."""
import json
from pathlib import Path


def fmt_timestamp(seconds: float) -> str:
    total_sec = int(round(seconds))
    hrs = total_sec // 3600
    mins = (total_sec % 3600) // 60
    secs = total_sec % 60
    if hrs > 0:
        return f"{hrs:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def run(shoot: str, job: Path, plan: dict) -> list:
    out = job / "out"
    out.mkdir(parents=True, exist_ok=True)

    chapters_text = []
    for ch in plan.get("chapters", []):
        ts = fmt_timestamp(ch["at"])
        chapters_text.append(f"{ts} - {ch['title']}")

    chapter_block = "\n".join(chapters_text) if chapters_text else "00:00 - Walk Begins"

    title = f"Singapore 4K Walking Tour: {shoot} | Stroll & Savor"

    desc = f"""Join us on an immersive 4K walking tour through {shoot}, Singapore.
Experience the authentic neighborhood sights, culinary landmarks, and ambient street atmosphere.

📍 Route & Timestamps:
{chapter_block}

🧭 About Stroll & Savor:
We track airline miles, food destinations, and authentic walking culture in Singapore and beyond.
Website: https://strollsavor.thethinkthank.com
Instagram: https://www.instagram.com/stroll_savor/
TikTok: https://www.tiktok.com/@stroll_savor
YouTube: https://www.youtube.com/@StrollAndSavor

🎧 Audio: Authentic natural ambient audio (no narration). Headphones recommended.
📹 Video: 4K Ultra HD 60fps walking tour.

#Singapore #WalkingTour #SingaporeWalk #4KWalk #StrollAndSavor #SingaporeFood
"""

    package = {
        "title": title,
        "description": desc,
        "chapters": plan.get("chapters", []),
        "tags": [
            "Singapore walking tour",
            "4K walking tour",
            "Singapore 4K",
            "Singapore walk",
            "Stroll and Savor",
            "Singapore street walk",
            "relaxing walk",
            "ambient walking tour",
            shoot,
        ],
    }

    pkg_json_file = out / "youtube_package.json"
    pkg_md_file = out / "youtube_package.md"

    pkg_json_file.write_text(json.dumps(package, indent=2, ensure_ascii=False))

    md_content = f"""# YouTube Publication Package: {shoot}

## Video Title
`{title}`

## Description & Timestamps
```
{desc}
```

## Recommended Tags
`{", ".join(package["tags"])}`
"""
    pkg_md_file.write_text(md_content)

    return [pkg_json_file, pkg_md_file]
