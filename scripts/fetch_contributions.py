#!/usr/bin/env python3
"""Scrape GitHub contribution calendar (no token needed) and write data/contributions.json."""

import json
import os
import sys
from datetime import date, timedelta

import requests
from bs4 import BeautifulSoup

USERNAME = "Mr-IR0k-oo1"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def fetch_contributions() -> list[dict]:
    url = f"https://github.com/users/{USERNAME}/contributions"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    days = []

    for rect in soup.select("td.ContributionCalendar-day"):
        level = rect.get("data-level")
        date_str = rect.get("data-date")
        if level is None or date_str is None:
            continue
        # Some cells are empty future dates — skip those
        tooltip = rect.find("tool-tip")
        count_text = tooltip.get_text(strip=True).split()[0] if tooltip else "0"
        try:
            count = int(count_text.replace(",", ""))
        except ValueError:
            count = 0

        days.append({
            "date": date_str,
            "count": count,
            "level": int(level),
        })

    return days


def compute_stats(days: list[dict]) -> dict:
    dates = [d["date"] for d in days]
    counts = {d["date"]: d["count"] for d in days}

    if not dates:
        return {}

    total = sum(counts.values())

    # Current streak (from today backward)
    today = date.today()
    streak = 0
    d = today
    while d.isoformat() in counts and counts[d.isoformat()] > 0:
        streak += 1
        d -= timedelta(days=1)

    # Longest streak
    longest = 0
    cur = 0
    for day in days:
        if day["count"] > 0:
            cur += 1
            longest = max(longest, cur)
        else:
            cur = 0

    # Best day
    best = max(days, key=lambda d: d["count"])

    # Monthly totals
    monthly = {}
    for day in days:
        month = day["date"][:7]  # YYYY-MM
        monthly[month] = monthly.get(month, 0) + day["count"]

    return {
        "total": total,
        "current_streak": streak,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "monthly": monthly,
    }


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    days = fetch_contributions()
    if not days:
        print("No contribution data found. Check username or GitHub availability.", file=sys.stderr)
        sys.exit(1)

    stats = compute_stats(days)
    payload = {
        "username": USERNAME,
        "fetched_at": date.today().isoformat(),
        "days": days,
        "stats": stats,
    }

    out = os.path.join(DATA_DIR, "contributions.json")
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"Wrote {out} — {stats.get('total', 0)} contributions, "
          f"{stats.get('current_streak', 0)} day streak")


if __name__ == "__main__":
    main()
