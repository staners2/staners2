#!/usr/bin/env python3
"""Build theme-aware SVG headers and a local preview using GitHub-rendered Markdown."""

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
    if compact:
        return f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="340" viewBox="0 0 680 340" role="img" aria-labelledby="title desc">
  <title id="title">Dima Aratin — DevOps engineer</title>
  <desc id="desc">Kubernetes, automation and integrations.</desc>
  <rect width="680" height="340" rx="18" fill="{palette['base']}"/>
  <path d="M530 0H662Q680 0 680 18V322Q680 340 662 340H530Z" fill="{palette['panel']}"/>
  <g fill="none" stroke="{palette['line']}" stroke-width="2">
    <path d="M560 46H630V111H600V171H648V284H560"/>
    <circle cx="560" cy="46" r="6" fill="{palette['base']}"/>
    <circle cx="560" cy="284" r="6" fill="{palette['base']}"/>
  </g>
  <path d="M38 60H72" stroke="{palette['accent']}" stroke-width="4" stroke-linecap="round"/>
  <g font-family="Arial, Helvetica, sans-serif">
    <text x="86" y="67" fill="{palette['muted']}" font-size="24">@staners2</text>
    <text x="34" y="154" fill="{palette['ink']}" font-size="68" font-weight="700" letter-spacing="-2">Dima Aratin</text>
    <text x="38" y="208" fill="{palette['ink']}" font-size="36">DevOps engineer</text>
    <text x="38" y="280" fill="{palette['muted']}" font-size="24">Kubernetes, automation</text>
    <text x="38" y="311" fill="{palette['muted']}" font-size="24">&amp; integrations.</text>
  </g>
</svg>
'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="340" viewBox="0 0 1200 340" role="img" aria-labelledby="title desc">
  <title id="title">Dima Aratin — DevOps engineer</title>
  <desc id="desc">Kubernetes, automation and integrations. A diagram connects code, a delivery pipeline and a Kubernetes cluster.</desc>
  <defs>
    <pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse">
      <circle cx="1" cy="1" r="1" fill="{palette['line']}" opacity=".52"/>
    </pattern>
  </defs>
  <rect width="1200" height="340" rx="18" fill="{palette['base']}"/>
  <path d="M670 0H1182Q1200 0 1200 18V322Q1200 340 1182 340H670Z" fill="{palette['panel']}"/>
  <path d="M670 0H1182Q1200 0 1200 18V322Q1200 340 1182 340H670Z" fill="url(#grid)"/>
  <path d="M56 64H98" stroke="{palette['accent']}" stroke-width="4" stroke-linecap="round"/>
  <g font-family="Arial, Helvetica, sans-serif">
    <text x="112" y="70" fill="{palette['muted']}" font-size="19">@staners2</text>
    <text x="52" y="155" fill="{palette['ink']}" font-size="66" font-weight="700" letter-spacing="-2">Dima Aratin</text>
    <text x="56" y="205" fill="{palette['ink']}" font-size="30">DevOps engineer</text>
    <text x="56" y="276" fill="{palette['muted']}" font-size="21">Kubernetes, automation &amp; integrations.</text>
    <text x="736" y="72" fill="{palette['muted']}" font-size="17">Code</text>
    <text x="920" y="72" fill="{palette['muted']}" font-size="17">CI/CD</text>
    <text x="928" y="222" fill="{palette['muted']}" font-size="17">Kubernetes</text>
  </g>
  <g fill="none" stroke="{palette['accent']}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
    <rect x="714" y="92" width="90" height="68" rx="10" fill="{palette['base']}"/>
    <circle cx="744" cy="112" r="5"/>
    <circle cx="744" cy="141" r="5"/>
    <circle cx="776" cy="112" r="5"/>
    <path d="M744 117V136M771 112H763Q754 112 754 124V127Q754 134 744 134"/>
    <path d="M804 126H903M897 121L903 126L897 131"/>
    <rect x="912" y="92" width="90" height="68" rx="10" fill="{palette['base']}"/>
    <path d="M930 110H951M930 125H970M930 140H961"/>
    <path d="M1002 126H1084Q1098 126 1098 140V215Q1098 238 1075 238H1002M1008 233L1002 238L1008 243"/>
    <path d="M826 215V271M826 243H912M860 243V215M892 243V271"/>
  </g>
  <g fill="{palette['base']}" stroke="{palette['line']}" stroke-width="2">
    <rect x="714" y="193" width="146" height="43" rx="7"/>
    <rect x="714" y="255" width="178" height="43" rx="7"/>
    <rect x="912" y="236" width="90" height="62" rx="10" stroke="{palette['accent']}" stroke-width="2.5"/>
  </g>
  <g font-family="Arial, Helvetica, sans-serif" font-size="16" fill="{palette['muted']}">
    <text x="732" y="220">Containers</text>
    <text x="732" y="282">Helm releases</text>
  </g>
  <g fill="{palette['accent']}">
    <rect x="930" y="253" width="12" height="12" rx="2"/>
    <rect x="952" y="253" width="12" height="12" rx="2"/>
    <rect x="974" y="253" width="12" height="12" rx="2"/>
    <rect x="930" y="276" width="12" height="6" rx="2" opacity=".5"/>
    <rect x="952" y="276" width="12" height="6" rx="2" opacity=".5"/>
    <rect x="974" y="276" width="12" height="6" rx="2" opacity=".5"/>
  </g>
  <circle cx="981" cy="111" r="4" fill="{palette['warm']}"/>
</svg>
'''


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
    (ROOT / "preview.html").write_text(PREVIEW.replace("__MARKDOWN__", rendered))
    print("Built four SVG headers and preview.html")


if __name__ == "__main__":
    main()
