#!/usr/bin/env python3
"""Fetch public GitHub profile stats + top languages (no token needed).

Writes data/stats.json. Uses only the public REST API (unauthenticated limit
is 60 req/hr — a daily cron is well within budget).
"""

import json
import os
import sys
from datetime import datetime, timezone

import requests

USERNAME = "Mr-IR0k-oo1"
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
BASE = "https://api.github.com"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/vnd.github+json",
}


def get_json(url: str) -> dict | list:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    return resp.json()


def fetch_repos() -> list[dict]:
    repos = []
    page = 1
    while True:
        url = f"{BASE}/users/{USERNAME}/repos?per_page=100&page={page}&sort=pushed"
        resp = requests.get(url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
        batch = resp.json()
        if not batch:
            break
        repos.extend(batch)
        if 'rel="next"' not in resp.headers.get("Link", ""):
            break
        page += 1
    return repos


def fetch_languages(repos: list[dict]) -> dict[str, int]:
    langs: dict[str, int] = {}
    for repo in repos:
        if repo.get("fork") or repo.get("archived"):
            continue
        try:
            data = get_json(f"{BASE}/repos/{USERNAME}/{repo['name']}/languages")
        except requests.RequestException:
            continue
        for lang, size in data.items():
            langs[lang] = langs.get(lang, 0) + size
    return langs


def main():
    os.makedirs(DATA_DIR, exist_ok=True)

    user = get_json(f"{BASE}/users/{USERNAME}")
    repos = fetch_repos()
    langs = fetch_languages(repos)

    total_stars = sum(r.get("stargazers_count", 0) for r in repos)
    total_forks = sum(r.get("forks_count", 0) for r in repos)

    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "user": {
            "name": user.get("name") or USERNAME,
            "bio": user.get("bio"),
            "location": user.get("location"),
            "followers": user.get("followers", 0),
            "following": user.get("following", 0),
            "public_repos": user.get("public_repos", 0),
            "created_at": user.get("created_at", ""),
        },
        "repos": {
            "count": len(repos),
            "total_stars": total_stars,
            "total_forks": total_forks,
        },
        "languages": langs,
    }

    out = os.path.join(DATA_DIR, "stats.json")
    with open(out, "w") as f:
        json.dump(payload, f, indent=2)

    print(
        f"Wrote {out} — {payload['user']['followers']} followers, "
        f"{total_stars} stars, {len(langs)} languages"
    )


if __name__ == "__main__":
    main()
