"""
Seed bucket list destinations and user bucket list items.

Usage:
    python scripts/seed_bucket_list.py <user_id>

Example:
    python scripts/seed_bucket_list.py xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
"""

import asyncio
import sys

import httpx

BASE_URL = "http://localhost:8000/api/v1"

# ── Destination definitions ────────────────────────────────────────────────────

VISITED_DESTINATIONS = [
    dict(name="Machu Picchu",  country="Peru",             continent="South America", category="HISTORY",   description="Ancient Incan citadel set high in the Andes Mountains."),
    dict(name="Cusco",         country="Peru",             continent="South America", category="HISTORY",   description="Former capital of the Inca Empire, rich with temples and colonial architecture."),
    dict(name="Lima",          country="Peru",             continent="South America", category="CITY",      description="Peru's vibrant coastal capital, known for world-class cuisine and history."),
    dict(name="Arequipa",      country="Peru",             continent="South America", category="CITY",      description="The White City, framed by three towering volcanoes."),
    dict(name="Huaraz",        country="Peru",             continent="South America", category="ADVENTURE", description="Gateway to the Cordillera Blanca, a trekker's paradise in the Andes."),
    dict(name="Tarapoto",      country="Peru",             continent="South America", category="NATURE",    description="Tropical city in the San Martin region, known for waterfalls and jungle landscapes."),
    dict(name="Ica",           country="Peru",             continent="South America", category="ADVENTURE", description="Desert oasis famous for the Huacachina lagoon and sand dune boarding."),
    dict(name="Oxapampa",      country="Peru",             continent="South America", category="NATURE",    description="Peaceful cloud forest town with Austrian-influenced architecture and coffee farms."),
    dict(name="Santiago de los Caballeros", country="Dominican Republic", continent="North America", category="CITY", description="The second-largest city in the Dominican Republic, known for its culture and nightlife."),
    dict(name="Santo Domingo", country="Dominican Republic", continent="North America", category="HISTORY", description="The oldest permanently inhabited European settlement in the Americas."),
]

DREAMING_DESTINATIONS = [
    dict(name="Japan",         country="Japan",            continent="Asia",          category="CULTURE",   description="A seamless blend of ancient tradition and cutting-edge modernity."),
    dict(name="South Korea",   country="South Korea",      continent="Asia",          category="CULTURE",   description="K-culture, street food, palaces, and neon-lit cities."),
    dict(name="Patagonia",     country="Argentina/Chile",  continent="South America", category="NATURE",    description="Dramatic end-of-the-world landscapes of glaciers, peaks, and wind-swept plains."),
    dict(name="Brazil",        country="Brazil",           continent="South America", category="NATURE",    description="Amazon rainforest, Carnival, pristine beaches, and samba."),
    dict(name="Milan",         country="Italy",            continent="Europe",        category="CITY",      description="Global capital of fashion and design, with Renaissance art around every corner."),
    dict(name="Spain",         country="Spain",            continent="Europe",        category="CULTURE",   description="Flamenco, tapas, Gaudí, and centuries of art and architecture."),
    dict(name="Portugal",      country="Portugal",         continent="Europe",        category="COAST",     description="Fado music, pastel de nata, dramatic cliffs, and golden Atlantic coastline."),
]


async def seed(user_id: str) -> None:
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30) as client:

        # ── Fetch reference data ───────────────────────────────────────────────

        cats_resp = await client.get("/destination-categories")
        cats_resp.raise_for_status()
        categories = {c["name"]: c["id"] for c in cats_resp.json()}
        print(f"Categories loaded: {list(categories.keys())}")

        statuses_resp = await client.get("/bucket-list-statuses")
        statuses_resp.raise_for_status()
        statuses = {s["name"]: s["id"] for s in statuses_resp.json()}
        print(f"Statuses loaded: {list(statuses.keys())}")

        visited_id = statuses["VISITED"]
        dreaming_id = statuses["DREAMING"]

        # ── Create destinations + bucket list items ────────────────────────────

        print("\n── Creating VISITED destinations ─────────────────────────────")
        for d in VISITED_DESTINATIONS:
            category_id = categories.get(d["category"])
            dest_resp = await client.post("/destinations", json={
                "name": d["name"],
                "country": d["country"],
                "continent": d["continent"],
                "description": d["description"],
                "category_id": category_id,
            })
            dest_resp.raise_for_status()
            destination = dest_resp.json()
            print(f"  ✓ {destination['name']} ({destination['country']})")

            item_resp = await client.post(f"/users/{user_id}/bucket-list", json={
                "destination_id": destination["id"],
                "status_id": visited_id,
            })
            item_resp.raise_for_status()

        print("\n── Creating DREAMING destinations ────────────────────────────")
        for d in DREAMING_DESTINATIONS:
            category_id = categories.get(d["category"])
            dest_resp = await client.post("/destinations", json={
                "name": d["name"],
                "country": d["country"],
                "continent": d["continent"],
                "description": d["description"],
                "category_id": category_id,
            })
            dest_resp.raise_for_status()
            destination = dest_resp.json()
            print(f"  ✓ {destination['name']} ({destination['country']})")

            item_resp = await client.post(f"/users/{user_id}/bucket-list", json={
                "destination_id": destination["id"],
                "status_id": dreaming_id,
            })
            item_resp.raise_for_status()

        print(f"\n✓ Done — {len(VISITED_DESTINATIONS)} visited, {len(DREAMING_DESTINATIONS)} dreaming")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/seed_bucket_list.py <user_id>")
        sys.exit(1)
    asyncio.run(seed(sys.argv[1]))
