#!/usr/bin/env python3
"""Build illustrated SVG assets and a local preview using GitHub-rendered Markdown."""

import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    "light": {
        "base": "#f5f8fc", "panel": "#eaf0f9", "ink": "#182c4a",
        "muted": "#526680", "line": "#ccd8e8", "accent": "#275dcc",
        "warm": "#aa6715",
    },
    "dark": {
        "base": "#14233b", "panel": "#1d304d", "ink": "#edf3fc",
        "muted": "#a8bad3", "line": "#365170", "accent": "#83b1ff",
        "warm": "#efbb73",
    },
}


def header(palette: dict[str, str], compact: bool = False) -> str:
    width, height = (680, 560) if compact else (1200, 380)
    left = 38 if compact else 52
    art_position = "translate(60 250)" if compact else "translate(650 46)"
    route = "M144 136H178Q198 136 198 116V104Q198 84 218 84H250V110H324Q346 110 346 132V186Q346 208 368 208H417"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">Dima Aratin — DevOps engineer</title>
  <desc id="desc">Kubernetes, automation and integrations. An illustrated delivery path connects a code terminal, a container image and a Kubernetes cluster.</desc>
  <style>
    .delivery-signal {{ stroke-dasharray:6 94; animation:delivery 8s linear infinite; }}
    @keyframes delivery {{
      0% {{ stroke-dashoffset:100; opacity:0; }}
      8%,88% {{ opacity:1; }}
      100% {{ stroke-dashoffset:0; opacity:0; }}
    }}
    @media (prefers-reduced-motion:reduce) {{ .delivery-signal {{ animation:none; opacity:0; }} }}
  </style>
  <defs>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{palette['line']}" opacity=".55"/>
    </pattern>
    <g id="container" stroke="{palette['accent']}" stroke-width="1.7" stroke-linejoin="round">
      <path d="M-42-3V39L0 62V20Z" fill="{palette['panel']}"/>
      <path d="M42-3V39L0 62V20Z" fill="{palette['base']}"/>
      <path d="M0-26 42-3 0 20-42-3Z" fill="{palette['panel']}"/>
      <path d="M0-26 42-3 0 20-42-3Z" fill="{palette['accent']}" opacity=".12" stroke="none"/>
      <path d="M-28 7V33M-14 15V41M14 15V41M28 7V33" fill="none" opacity=".5"/>
      <path d="M-21-15 21 8" fill="none" opacity=".5"/>
    </g>
  </defs>
  <rect x=".75" y=".75" width="{width - 1.5}" height="{height - 1.5}" rx="20" fill="{palette['base']}" stroke="{palette['line']}" stroke-width="1.5"/>
  <rect x="{24 if compact else 632}" y="{248 if compact else 24}" width="{width - (48 if compact else 656)}" height="{height - (272 if compact else 48)}" rx="16" fill="{palette['panel']}"/>
  <rect x="{24 if compact else 632}" y="{248 if compact else 24}" width="{width - (48 if compact else 656)}" height="{height - (272 if compact else 48)}" rx="16" fill="url(#grid)"/>
  <path d="M{left} {52 if compact else 65}h34" stroke="{palette['accent']}" stroke-width="4" stroke-linecap="round"/>
  <g font-family="Arial, Helvetica, sans-serif">
    <text x="{left + 48}" y="{59 if compact else 72}" fill="{palette['muted']}" font-size="{23 if compact else 19}">@staners2</text>
    <text x="{left - 3}" y="{130 if compact else 156}" fill="{palette['ink']}" font-size="{66 if compact else 68}" font-weight="700" letter-spacing="-2">Dima Aratin</text>
    <text x="{left}" y="{177 if compact else 210}" fill="{palette['ink']}" font-size="{32 if compact else 31}">DevOps engineer</text>
    <text x="{left}" y="{221 if compact else 285}" fill="{palette['muted']}" font-size="{23 if compact else 22}">Kubernetes, automation &amp; integrations.</text>
  </g>
  <g transform="{art_position}">
    <g fill="{palette['muted']}" font-family="Arial, Helvetica, sans-serif" font-size="20" text-anchor="middle">
      <text x="84" y="32">Code</text>
      <text x="250" y="32">CI/CD</text>
      <text x="414" y="286">Kubernetes</text>
    </g>
    <path d="{route}" fill="none" stroke="{palette['accent']}" stroke-width="2.5" opacity=".38"/>
    <path d="{route}" pathLength="100" class="delivery-signal" fill="none" stroke="{palette['warm']}" stroke-width="4" stroke-linecap="round"/>
    <g transform="rotate(-7 84 124)">
      <rect x="28" y="76" width="132" height="112" rx="12" fill="{palette['line']}"/>
      <rect x="20" y="68" width="132" height="112" rx="12" fill="{palette['base']}" stroke="{palette['accent']}" stroke-width="1.8"/>
      <path d="M21 95H151" stroke="{palette['line']}" stroke-width="1.5"/>
      <g fill="{palette['line']}"><circle cx="35" cy="82" r="3"/><circle cx="47" cy="82" r="3"/><circle cx="59" cy="82" r="3"/></g>
      <path d="M38 114 48 122 38 130M59 131H83" fill="none" stroke="{palette['warm']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M38 149H95M38 161H75" stroke="{palette['accent']}" stroke-width="3" stroke-linecap="round" opacity=".5"/>
    </g>
    <ellipse cx="250" cy="166" rx="60" ry="16" fill="{palette['line']}" opacity=".4"/>
    <use href="#container" transform="translate(250 87) scale(1.1)"/>
    <path d="M233 82 244 88 267 75" fill="none" stroke="{palette['warm']}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M324 198V211L414 263 504 211V198" fill="{palette['base']}" stroke="{palette['line']}" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M414 147 504 198 414 250 324 198Z" fill="{palette['base']}" stroke="{palette['accent']}" stroke-width="1.8" stroke-linejoin="round"/>
    <path d="M369 173 459 224M369 224 459 173" stroke="{palette['line']}" stroke-width="1.5"/>
    <use href="#container" transform="translate(383 155) scale(.65)"/>
    <use href="#container" transform="translate(444 189) scale(.65)"/>
    <use href="#container" transform="translate(383 216) scale(.65)"/>
    <g fill="{palette['warm']}"><circle cx="399" cy="171" r="2.5"/><circle cx="460" cy="205" r="2.5"/><circle cx="399" cy="232" r="2.5"/></g>
  </g>
</svg>
'''


def technology_strip(palette: dict[str, str], compact: bool = False) -> str:
    icons = (
        ("Kubernetes", '<path d="M24 3 42 13V35L24 45 6 35V13Z"/><circle cx="24" cy="24" r="8"/><path d="M24 7V16M24 32V41M9 15 17 20M31 28 39 33M9 33 17 28M31 20 39 15M7 24H16M32 24H41"/>'),
        ("Docker", '<path d="M5 25H36Q40 25 42 21L46 23Q44 30 36 31Q31 41 19 41Q7 41 5 25Z"/><path d="M8 17H15V24H8ZM17 17H24V24H17ZM26 17H33V24H26ZM17 8H24V15H17ZM26 8H33V15H26Z"/><circle cx="12" cy="31" r="1"/>'),
        ("GitLab CI", '<path d="M24 43 4 28 9 5 17 20H31L39 5 44 28Z"/><path d="M4 28 17 20 24 43 31 20 44 28M9 5 17 20M39 5 31 20"/>'),
        ("Actions", '<circle cx="10" cy="9" r="6"/><circle cx="37" cy="24" r="6"/><circle cx="10" cy="39" r="6"/><path d="M10 15V33M16 9H21Q27 9 27 16V17Q27 24 31 24M16 39H21Q27 39 27 32V31Q27 24 31 24"/>'),
        ("Python", '<path d="M24 24H12Q6 24 6 17V12Q6 5 13 5H27Q34 5 34 12V18H20Q14 18 14 25V33H7M24 24H36Q42 24 42 31V36Q42 43 35 43H21Q14 43 14 36V30H28Q34 30 34 23V15H41"/><circle cx="15" cy="11" r="1"/><circle cx="33" cy="37" r="1"/>'),
        ("Go", '<path d="M2 15H12M0 23H9M4 31H12"/><text x="13" y="34" stroke="none" fill="currentColor" font-family="Arial, Helvetica, sans-serif" font-size="28" font-weight="700" font-style="italic">Go</text>'),
        ("PostgreSQL", '<path d="M24 5Q9 3 7 17Q5 29 14 35L18 29M24 5Q39 3 41 17Q43 29 34 35L30 29M18 15Q24 11 30 15V36Q30 43 24 43Q20 43 20 38M18 15V27Q18 32 24 32Q30 32 34 28M12 16 15 25M36 16 33 25"/><circle cx="20" cy="20" r="1"/><circle cx="28" cy="20" r="1"/>'),
    )
    width, height = (680, 276) if compact else (1200, 148)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
             '<title id="title">Tools I work with</title>',
             '<desc id="desc">Illustrated icons for Kubernetes, Docker, GitLab CI, GitHub Actions, Python, Go and PostgreSQL.</desc>',
             f'<rect width="{width}" height="{height}" rx="16" fill="{palette["base"]}"/>']
    for index, (label, drawing) in enumerate(icons):
        if compact:
            row, column = divmod(index, 4)
            x = (100 if row == 0 else 180) + column * 160
            y = 22 + row * 132
        else:
            x, y = 96 + index * 168, 22
        parts.append(f'<g transform="translate({x - 29} {y}) scale(1.2)" fill="none" stroke="{palette["accent"]}" color="{palette["accent"]}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{drawing}</g>')
        parts.append(f'<text x="{x}" y="{y + 87}" fill="{palette["ink"]}" font-family="Arial, Helvetica, sans-serif" font-size="22" text-anchor="middle">{label}</text>')
    parts.append('</svg>\n')
    return '\n'.join(parts)


PREVIEW = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>staners2 — GitHub README preview</title>
<style>
:root { --bg:#ffffff; --ink:#1f2328; --muted:#59636e; --line:#d1d9e0; --soft:#f6f8fa; --link:#0969da; color-scheme:light; }
:root[data-theme="dark"] { --bg:#0d1117; --ink:#f0f6fc; --muted:#9198a1; --line:#3d444d; --soft:#151b23; --link:#4493f8; color-scheme:dark; }
* { box-sizing:border-box; }
body { margin:0; background:var(--soft); color:var(--ink); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif; }
.controls { display:flex; flex-wrap:wrap; gap:16px; align-items:center; padding:16px 24px; border-bottom:1px solid var(--line); background:var(--bg); }
.controls strong { margin-right:auto; font-size:14px; }
.controls label { font-size:13px; display:flex; align-items:center; gap:8px; }
select { background:var(--soft); color:var(--ink); border:1px solid var(--line); border-radius:6px; padding:6px 8px; font:inherit; }
select:focus-visible { outline:2px solid var(--link); outline-offset:2px; }
.note { margin:18px auto; padding:0 20px; max-width:1012px; color:var(--muted); font-size:13px; line-height:1.5; }
main { width:calc(100% - 40px); max-width:972px; margin:0 auto 48px; background:var(--bg); border:1px solid var(--line); border-radius:6px; }
.file { padding:12px 24px; border-bottom:1px solid var(--line); font:12px ui-monospace,SFMono-Regular,Consolas,monospace; color:var(--muted); }
article { padding:28px 32px; font-size:16px; line-height:1.5; overflow-wrap:break-word; }
article > :first-child { margin-top:0; }
p { margin:0 0 16px; }
picture, themed-picture { display:block; }
img { display:block; max-width:100%; height:auto; }
a { color:var(--link); text-decoration:none; }
a:hover { text-decoration:underline; }
a:focus-visible { outline:2px solid var(--link); outline-offset:3px; }
h3 { margin:24px 0 16px; font-size:20px; font-weight:600; line-height:1.25; }
code { font:85% ui-monospace,SFMono-Regular,Consolas,monospace; background:var(--soft); border-radius:6px; padding:.2em .4em; }
markdown-accessiblity-table { display:block; overflow-x:auto; margin-bottom:16px; }
table { border-spacing:0; border-collapse:collapse; width:100%; font-size:14px; }
th,td { padding:9px 13px; border:1px solid var(--line); text-align:left; }
th { font-weight:600; }
tr:nth-child(2n) { background:var(--soft); }
ul { padding-left:24px; margin:0 0 16px; }
li + li { margin-top:8px; }
hr { height:1px; margin:24px 0; padding:0; border:0; background:var(--line); }
@media(max-width:600px) { .controls { padding:12px; gap:12px; } .controls strong { width:100%; } main { width:calc(100% - 24px); } article { padding:16px; } .file { padding:12px 16px; } .note { padding:0 12px; } }
</style>
</head>
<body>
<div class="controls">
  <strong>staners2 / README.md</strong>
  <label>Theme <select id="theme"><option value="light">Light</option><option value="dark">Dark</option></select></label>
  <label>Width <select id="width"><option value="972">Desktop</option><option value="390">Mobile · 390 px</option></select></label>
</div>
<p class="note">Local preview of GitHub-rendered Markdown. Theme and width controls belong to this preview; the profile will use GitHub’s interface.</p>
<main><div class="file">staners2/README.md</div><article>__MARKDOWN__</article></main>
<script>
const theme = document.querySelector('#theme');
const width = document.querySelector('#width');
const pictures = [...document.querySelectorAll('article picture')].map(picture => ({
  image: picture.querySelector('img'),
  sources: [...picture.querySelectorAll('source')].map(source => ({ source, media: source.media })),
}));
function updatePreview() {
  document.documentElement.dataset.theme = theme.value;
  document.querySelector('main').style.maxWidth = `${width.value}px`;
  // GitHub switches themed pictures itself; the local selector needs to do it explicitly.
  const compact = width.value === '390' || matchMedia('(max-width: 600px)').matches;
  pictures.forEach(picture => {
    const selected = picture.sources.find(item =>
      item.media.includes(`prefers-color-scheme: ${theme.value}`) &&
      (compact || !item.media.includes('max-width')));
    picture.image.src = selected.source.srcset;
    picture.sources.forEach(item => { item.source.media = 'not all'; });
  });
}
theme.value = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
theme.addEventListener('change', updatePreview);
width.addEventListener('change', updatePreview);
matchMedia('(max-width: 600px)').addEventListener('change', updatePreview);
updatePreview();
</script>
</body>
</html>
'''


def main() -> None:
    payload = json.dumps({"text": (ROOT / "README.md").read_text(), "mode": "gfm"}).encode()
    request = urllib.request.Request(
        "https://api.github.com/markdown", data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "staners2-profile-preview"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            rendered = response.read().decode()
    except (urllib.error.URLError, TimeoutError) as error:
        raise SystemExit(f"GitHub Markdown rendering failed: {error}") from error

    assets = ROOT / "assets"
    assets.mkdir(exist_ok=True)
    for theme, palette in PALETTES.items():
        (assets / f"header-{theme}.svg").write_text(header(palette))
        (assets / f"header-mobile-{theme}.svg").write_text(header(palette, compact=True))
        (assets / f"stack-{theme}.svg").write_text(technology_strip(palette))
        (assets / f"stack-mobile-{theme}.svg").write_text(technology_strip(palette, compact=True))
    (ROOT / "preview.html").write_text(PREVIEW.replace("__MARKDOWN__", rendered))
    print("Built four animated headers, four technology strips and preview.html")


if __name__ == "__main__":
    main()
