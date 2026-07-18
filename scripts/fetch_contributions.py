#!/usr/bin/env python3
"""Scrape GitHub contribution calendar (no token needed) and write data/contributions.json."""

import json
import os
import re
import sys
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = "Mr-IR0k-oo1"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def fetch_contributions() -> tuple[list[dict], int]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    # Extract total from the heading (e.g. "778 contributions in the last year")
    total = 0
    for heading in soup.find_all(["h2", "h3"]):
        text = heading.get_text(strip=True)
        match = re.search(r"([\d,]+)\s+contributions", text)
        if match:
            total = int(match.group(1).replace(",", ""))
            break

    # Collect cells, deduplicating by date
    seen = set()
    days = []
    for cell in soup.select("td.ContributionCalendar-day"):
        level = cell.get("data-level")
        date_str = cell.get("data-date")
        if level is None or date_str is None:
            continue
        if date_str in seen:
            continue
        seen.add(date_str)
        days.append({
            "date": date_str,
            "level": int(level),
        })

    # Sort chronologically
    days.sort(key=lambda d: d["date"])

    # Estimate counts from levels (exact counts no longer in HTML)
    LEVEL_ESTIMATES = {0: 0, 1: 2, 2: 5, 3: 8, 4: 12}
    for d in days:
        d["count"] = LEVEL_ESTIMATES.get(d["level"], 0)

    return days, total


def compute_stats(days: list[dict], total: int) -> dict:
    if not days:
        return {}

    # Current streak (from today backward, using level > 0)
    today = date.today()
    streak = 0
    d = today
    active_dates = {d["date"] for d in days if d["level"] > 0}
    while d.isoformat() in active_dates:
        streak += 1
        d -= timedelta(days=1)

    # Longest streak
    longest = 0
    cur = 0
    for day in days:
        if day["level"] > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0

    # Best day (by level)
    best = max(days, key=lambda d: d["level"])

    # Monthly totals (estimated)
    monthly = {}
    for day in days:
        month = day["date"][:7]
        monthly[month] = monthly.get(month, 0) + day["count"]

    return {
        "total": total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "level": best["level"]},
        "monthly": monthly,
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    days, total = fetch_contributions()
    if not days:
        print("No contribution data found. Check username or GitHub availability.", file=sys.stderr)
        sys.exit(1)

    stats = compute_stats(days, total)
    payload = {
        "username": USERNAME,
        "fetched_at": date.today().isoformat(),
        "days": days,
        "stats": stats,
    }

    out = os.path.join(DATA_DIR, "contributions.json")
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {out} — {total:,} contributions, "
          f"{stats.get('current_streak', 0)} day streak")


if __name__ == "__main__":
    main()
