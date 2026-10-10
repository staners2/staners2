#!/usr/bin/env python3
"""Collect publicly visible GitHub activity and build profile statistics images."""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta, timezone
from html import escape
from html.parser import HTMLParser
import json
import os
import re
import urllib.parse
import urllib.request

from build_preview import PALETTES, ROOT

USERNAME = "staners2"


class CalendarParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cells = []
        self.tooltips = {}
        self.tooltip = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "data-date" in attrs:
            self.cells.append((attrs.get("id"), attrs["data-date"]))
        if tag == "tool-tip":
            self.tooltip = attrs.get("for")

    def handle_data(self, text):
        if self.tooltip:
            self.tooltips[self.tooltip] = self.tooltips.get(self.tooltip, "") + text

    def handle_endtag(self, tag):
        if tag == "tool-tip":
            self.tooltip = None


def parse_calendar(html: str) -> list[dict]:
    parser = CalendarParser()
    parser.feed(html)
    days = {}
    for cell_id, day in parser.cells:
        date.fromisoformat(day)
        if day in days:
            raise ValueError(f"Calendar contains a duplicate date: {day}")
        tooltip = parser.tooltips.get(cell_id, "").strip()
        if not tooltip:
            raise ValueError(f"Calendar tooltip missing for {day}")
        match = re.match(r"([\d,]+) contributions? on\b", tooltip)
        if tooltip.startswith("No contributions on "):
            count = 0
        elif match:
            count = int(match[1].replace(",", ""))
        else:
            raise ValueError(f"Calendar count format changed for {day}")
        days[day] = count
    if not days:
        raise ValueError("Calendar has no contribution dates")
    return [{"date": day, "count": count} for day, count in sorted(days.items())]


def summarize_repositories(repositories: list[dict]) -> dict:
    public = [repo for repo in repositories if not repo["private"]]
    originals = [repo for repo in public if not repo["fork"]]
    languages = Counter(repo["language"] for repo in originals if repo["language"])
    return {
        "public": len(public), "originals": len(originals),
        "forks": len(public) - len(originals), "languages": dict(languages),
    }


def search_total(response: dict) -> int:
    if response["incomplete_results"]:
        raise ValueError("GitHub search returned incomplete results")
    count = response["total_count"]
    if type(count) is not int or count < 0:
        raise ValueError("GitHub search returned an invalid total")
    return count


def fetch(url: str, *, as_json: bool = True):
    headers = {"User-Agent": "staners2-profile-stats", "Accept-Language": "en-US"}
    if url.startswith("https://api.github.com/"):
        headers["Accept"] = "application/vnd.github+json"
        if token := os.environ.get("GITHUB_TOKEN"):
            headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=30) as response:
        content = response.read().decode()
    return json.loads(content) if as_json else content


def collect_stats() -> dict:
    urls = {
        "calendar": f"https://github.com/users/{USERNAME}/contributions",
        "commits": "https://api.github.com/search/commits?" + urllib.parse.urlencode(
            {"q": f"author:{USERNAME} is:public", "per_page": 1}),
        "pull_requests": "https://api.github.com/search/issues?" + urllib.parse.urlencode(
            {"q": f"author:{USERNAME} type:pr is:public", "per_page": 1}),
        "repos": f"https://api.github.com/users/{USERNAME}/repos?type=owner&per_page=100&page=1",
    }
    with ThreadPoolExecutor(max_workers=4) as executor:
        pending = {name: executor.submit(fetch, url, as_json=name != "calendar")
                   for name, url in urls.items()}
        results = {name: future.result() for name, future in pending.items()}
    repositories = results["repos"]
    batch = repositories
    page = 2
    while len(batch) == 100:
        batch = fetch(urls["repos"].rsplit("&page=", 1)[0] + f"&page={page}")
        repositories.extend(batch)
        page += 1

    end = datetime.now(timezone.utc).date()
    start = end - timedelta(days=364)
    days = [day for day in parse_calendar(results["calendar"])
            if start.isoformat() <= day["date"] <= end.isoformat()]
    if len(days) != 365:
        raise ValueError(f"Expected 365 calendar days, received {len(days)}")
    return {
        "username": USERNAME, "updated": end.isoformat(),
        "period_start": start.isoformat(), "period_end": end.isoformat(),
        "contributions": sum(day["count"] for day in days),
        "public_commits": search_total(results["commits"]),
        "public_pull_requests": search_total(results["pull_requests"]),
        "repositories": summarize_repositories(repositories), "days": days,
    }


def dashboard(stats: dict, palette: dict[str, str], *, compact: bool = False) -> str:
    width, height = (680, 1100) if compact else (1200, 660)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">GitHub activity for Dima Aratin</title>',
             f'<desc id="desc">{stats["contributions"]} contributions in 365 days, {stats["public_commits"]} publicly indexed commits, {stats["repositories"]["originals"]} non-fork public repositories and {stats["public_pull_requests"]} public pull requests. Commit and pull request counts cover all time. Updated {stats["updated"]}.</desc>',
             f'<rect width="{width}" height="{height}" rx="18" fill="{palette["base"]}"/>',
             '<g font-family="Arial, Helvetica, sans-serif">']

    def text(x, y, value, size=20, *, color=None, weight=400, anchor="start"):
        parts.append(f'<text x="{x}" y="{y}" font-size="{size}" fill="{color or palette["ink"]}" font-weight="{weight}" text-anchor="{anchor}">{escape(str(value))}</text>')

    text(32, 48, "GitHub at a glance", 32 if compact else 28, weight=700)
    text(32 if compact else width - 32, 78 if compact else 47,
         f'Updated {stats["updated"]}', 21 if compact else 17,
         color=palette["muted"], anchor="start" if compact else "end")

    metrics = [
        (stats["contributions"], "Contributions", "Last 365 days"),
        (stats["public_commits"], "Public commits", "Indexed · all time"),
        (stats["repositories"]["originals"], "Original repos", "Public · no forks"),
        (stats["public_pull_requests"], "Pull requests", "Public · all time"),
    ]
    for index, (value, label, scope) in enumerate(metrics):
        x = 28 + (index % 2) * 322 if compact else 28 + index * 292
        y = 106 + (index // 2) * 155 if compact else 80
        card_width, card_height = (296, 137) if compact else (268, 128)
        parts.append(f'<rect x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="10" fill="{palette["panel"]}"/>')
        text(x + 20, y + 50, f"{value:,}", 44, color=palette["accent"], weight=700)
        text(x + 20, y + 87, label, 24 if compact else 22, weight=600)
        text(x + 20, y + 116, scope, 20 if compact else 17, color=palette["muted"])

    monthly = Counter()
    for day in stats["days"]:
        monthly[day["date"][:7]] += day["count"]
    months = sorted(monthly)
    chart_x, chart_y, chart_width, chart_height = (38, 532, 600, 170) if compact else (42, 338, 700, 192)
    heading_y = 463 if compact else 264
    text(chart_x, heading_y, "Contribution activity", 30 if compact else 26, weight=700)
    text(chart_x, heading_y + 29, "Monthly totals in the last 365 days", 21 if compact else 18, color=palette["muted"])
    peak = max(monthly.values(), default=0)
    step = chart_width / len(months)
    baseline = chart_y + chart_height
    for index, month in enumerate(months):
        value = monthly[month]
        bar_height = chart_height * value / max(peak, 1)
        x = chart_x + index * step
        parts.append(f'<rect x="{x:.1f}" y="{baseline - max(bar_height, 2):.1f}" width="{step - 10:.1f}" height="{max(bar_height, 2):.1f}" rx="4" fill="{palette["accent"]}" opacity="{0.9 if value else 0.2}"><title>{escape(month)}: {value} contributions</title></rect>')
        if value:
            text(x + (step - 10) / 2, baseline - bar_height - 10, value,
                 20 if compact else 16, color=palette["muted"], anchor="middle")
        if not compact or index % 3 == 0 or index == len(months) - 1:
            label = date.fromisoformat(month + "-01").strftime("%b")
            text(x + (step - 10) / 2, baseline + 28, label,
                 22 if compact else 16, color=palette["muted"], anchor="middle")
    active = sum(day["count"] > 0 for day in stats["days"])
    text(chart_x, baseline + 66, f'{active} active days · {stats["period_start"]} — {stats["period_end"]}',
         21 if compact else 18, color=palette["muted"])

    languages = sorted(stats["repositories"]["languages"].items(), key=lambda item: (-item[1], item[0]))
    if len(languages) > 8:
        languages = languages[:7] + [("Other", sum(count for _, count in languages[7:]))]
    language_x, language_y = (38, 824) if compact else (806, 264)
    text(language_x, language_y, "Repository languages", 30 if compact else 26, weight=700)
    text(language_x, language_y + 29, "Main language · non-fork repos", 21 if compact else 18, color=palette["muted"])
    most = max((count for _, count in languages), default=1)
    for index, (language, count) in enumerate(languages):
        x = 38 + (index // 4) * 322 if compact else language_x
        y = language_y + 73 + (index % 4) * 51 if compact else language_y + 76 + index * 36
        text(x, y, language, 24 if compact else 19)
        text(x + (280 if compact else 344), y, f'{count} {"repo" if count == 1 else "repos"}',
             21 if compact else 17, color=palette["muted"], anchor="end")
        bar_x, bar_y = (x, y + 12) if compact else (x + 124, y - 11)
        bar_width = 280 if compact else 154
        parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width}" height="5" rx="2.5" fill="{palette["line"]}"/>')
        parts.append(f'<rect x="{bar_x}" y="{bar_y}" width="{bar_width * count / most:.1f}" height="5" rx="2.5" fill="{palette["accent"]}"/>')
    parts.extend(['</g>', '</svg>'])
    return "\n".join(parts) + "\n"


def main() -> None:
    stats = collect_stats()
    images = {}
    for theme, palette in PALETTES.items():
        images[f"stats-{theme}.svg"] = dashboard(stats, palette)
        images[f"stats-mobile-{theme}.svg"] = dashboard(stats, palette, compact=True)
    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for name, content in images.items():
        (assets / name).write_text(content)
    (assets / "stats.json").write_text(json.dumps(stats, indent=2) + "\n")
    print(f'Updated public stats: {stats["contributions"]} contributions, '
          f'{stats["public_commits"]} indexed commits, '
          f'{stats["repositories"]["originals"]} original repos, '
          f'{stats["public_pull_requests"]} pull requests.')


if __name__ == "__main__":
    main()
