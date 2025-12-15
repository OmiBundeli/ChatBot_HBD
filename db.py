import sqlite3
from datetime import datetime

DB_PATH = "businesses.db"


def run_sql(sql: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        columns = [c[0] for c in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def rank_results(rows, top_n=10):
    """
    Correct ranking flow:
    - rank ALL rows first
    - then take top N
    """

    now = datetime.utcnow()
    ranked = []
    seen = set()

    for r in rows:
        # -------- filter permanently closed --------
        text = f"{r.get('name','')} {r.get('address','')}".lower()
        if "permanently closed" in text:
            continue

        # -------- deduplicate --------
        key = (
            (r.get("name") or "").lower().strip(),
            (r.get("address") or "").lower().strip()
        )
        if key in seen:
            continue
        seen.add(key)

        rating = r.get("reviews_average") or 0
        reviews = r.get("reviews_count") or 0

        # -------- confidence adjustment --------
        if reviews < 50:
            rating = (rating + 4.0) / 2

        # -------- scoring --------
        rating_score = rating * 0.6
        popularity_score = min(reviews, 1000) / 1000 * 0.35

        freshness_score = 0
        try:
            created = datetime.fromisoformat(r["created_at"])
            if (now - created).days <= 180:
                freshness_score = 0.05
        except Exception:
            pass

        r["score"] = round(
            rating_score + popularity_score + freshness_score, 3
        )
        ranked.append(r)

    # 🔥 rank FIRST
    ranked.sort(key=lambda x: x["score"], reverse=True)

    # 🔥 then slice
    return ranked[:top_n]
