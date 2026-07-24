#!/usr/bin/env python3
"""AIMAP hero image generator.

src/data/*.json (research/journals/conferences/projects)을 읽어 브랜드 톤
(버트 오렌지 #D2622B + 웜 차콜)의 히어로 SVG 3장을 그리고, 헤드리스 Chrome으로
PNG(2752x1536)로 렌더링해 public/images/hero/slide{1,2,3}.png 를 교체한다.

논문/데이터가 갱신되면 다시 실행하는 것만으로 히어로가 최신 내용을 반영한다:

    python3 hero-generator/generate_heroes.py

slide1: processing map 등고선 + 최적점 마커 (로고 세계관, PI의 가공성 맵 연구 오마주)
slide2: 압연 롤 → 노드 네트워크 (소성가공 헤리티지 x AI)
slide3: 연도별 논문 실적 막대 + 실제 논문 제목 텍스처 (데이터 기반, 자동 갱신)

주의: 히어로 위에 Vue 오버레이 타이틀이 화면 중앙에 얹히므로, 밝은 요소는
가장자리·하단에 배치하고 중앙부는 어둡게 비워 둔다.
"""

import json
import math
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "src" / "data"
OUT = ROOT / "public" / "images" / "hero"
WORK = pathlib.Path(__file__).resolve().parent / "build"

W, H = 2752, 1536
ORANGE = "#e0762f"
DEEP = "#d2622b"
RUST = "#b6491c"
EMBER = "#f0955c"
MUTED = "#8a7666"
FAINT = "#5e4f42"
FONT = "Pretendard, 'Helvetica Neue', Helvetica, Arial, sans-serif"

BG = f"""
  <defs>
    <radialGradient id="vig" cx="50%" cy="42%" r="80%">
      <stop offset="0" stop-color="#221913"/>
      <stop offset="0.55" stop-color="#171210"/>
      <stop offset="1" stop-color="#0e0b09"/>
    </radialGradient>
    <linearGradient id="strip" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{RUST}"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{EMBER}"/><stop offset="1" stop-color="{RUST}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{H}" fill="url(#vig)"/>
"""


def svg(name: str, body: str) -> pathlib.Path:
    WORK.mkdir(parents=True, exist_ok=True)
    path = WORK / f"{name}.svg"
    path.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'width="{W}" height="{H}">{BG}{body}</svg>'
    )
    return path


def contour_path(cx, cy, r, phases, samples=200):
    pts = []
    for i in range(samples + 1):
        t = 2 * math.pi * i / samples
        rr = r * (1 + 0.14 * math.sin(3 * t + phases[0]) + 0.07 * math.sin(5 * t + phases[1]))
        pts.append(f"{cx + rr * math.cos(t):.1f},{cy + rr * math.sin(t):.1f}")
    return "M" + " L".join(pts) + " Z"


def contour_cluster(cx, cy, scale=1.0, rings=7, base_opacity=0.75):
    parts = []
    for k in range(rings, 0, -1):
        r = 92 * k * scale
        op = base_opacity * (0.35 + 0.65 * (rings - k + 1) / rings)
        parts.append(
            f'<path d="{contour_path(cx, cy, r, (0.7 * k, 1.9 * k))}" fill="none" '
            f'stroke="{EMBER if k % 2 else DEEP}" stroke-width="{3.2 * scale:.1f}" opacity="{op:.2f}"/>'
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="{60 * scale:.0f}" fill="{RUST}" opacity="0.5"/>')
    return "".join(parts)


def marker(cx, cy, dx, dy, scale=1.0):
    return (
        f'<line x1="{cx}" y1="{cy}" x2="{cx + dx}" y2="{cy + dy}" stroke="#f4ede5" '
        f'stroke-width="{7 * scale:.0f}" stroke-linecap="round"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{16 * scale:.0f}" fill="#f4ede5"/>'
        f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{20 * scale:.0f}" fill="#f4ede5"/>'
    )


def load(name):
    return json.load(open(DATA / f"{name}.json"))


def slide1():
    body = []
    body.append(contour_cluster(660, 1120, 1.0))
    body.append(marker(660, 1120, 150, -95))
    body.append(contour_cluster(2430, 260, 0.42, rings=5, base_opacity=0.4))
    # processing-map 축 (PI의 가공성 맵 연구 오마주)
    body.append(
        f'<line x1="170" y1="1466" x2="1420" y2="1466" stroke="{MUTED}" stroke-width="3" opacity="0.6"/>'
        f'<line x1="170" y1="1466" x2="170" y2="560" stroke="{MUTED}" stroke-width="3" opacity="0.6"/>'
    )
    for i in range(9):
        x = 170 + i * 150
        body.append(f'<line x1="{x}" y1="1466" x2="{x}" y2="1482" stroke="{MUTED}" stroke-width="3" opacity="0.5"/>')
        y = 1466 - i * 110
        body.append(f'<line x1="154" y1="{y}" x2="170" y2="{y}" stroke="{MUTED}" stroke-width="3" opacity="0.5"/>')
    body.append(
        f'<text x="1430" y="1508" font-family="{FONT}" font-size="30" letter-spacing="6" '
        f'fill="{MUTED}" opacity="0.85" text-anchor="end">TEMPERATURE</text>'
        f'<text x="120" y="540" font-family="{FONT}" font-size="30" letter-spacing="6" '
        f'fill="{MUTED}" opacity="0.85" transform="rotate(-90 120 540)" text-anchor="end">LOG STRAIN RATE</text>'
    )
    # 우상단 희미한 노드 별자리
    nodes = [(2100, 620), (2300, 500), (2520, 590), (2650, 430)]
    for i in range(len(nodes) - 1):
        (x1, y1), (x2, y2) = nodes[i], nodes[i + 1]
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RUST}" stroke-width="3" opacity="0.35"/>')
    for x, y in nodes:
        body.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{EMBER}" opacity="0.5"/>')
    return "".join(body)


def slide2():
    body = []
    # 압연 롤 2개 + 판재
    strip_y, gap = 1160, 36
    for cy in (strip_y - 170 - gap, strip_y + 170 + gap):
        body.append(
            f'<circle cx="560" cy="{cy}" r="170" fill="#231b15" stroke="{RUST}" stroke-width="5" opacity="0.95"/>'
            f'<circle cx="560" cy="{cy}" r="52" fill="#0e0b09" stroke="{MUTED}" stroke-width="4" opacity="0.8"/>'
        )
    body.append(
        f'<path d="M40 {strip_y - 46} L440 {strip_y - 46} L700 {strip_y - 15} L1080 {strip_y - 15} '
        f'L1080 {strip_y + 15} L700 {strip_y + 15} L440 {strip_y + 46} L40 {strip_y + 46} Z" '
        f'fill="url(#strip)" opacity="0.95"/>'
    )
    # 판재가 노드 네트워크로 변환
    chain = [(1080, strip_y), (1310, 1090), (1560, 1020), (1830, 930), (2110, 820), (2380, 690)]
    for i in range(len(chain) - 1):
        (x1, y1), (x2, y2) = chain[i], chain[i + 1]
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{DEEP}" stroke-width="7" opacity="0.8"/>')
    for i, (x, y) in enumerate(chain[1:], 1):
        body.append(f'<circle cx="{x}" cy="{y}" r="17" fill="{EMBER if i % 2 else ORANGE}"/>')
    # 우상단 분기 별자리
    consts = [(2380, 690), (2530, 520), (2680, 600), (2560, 350), (2700, 240)]
    links = [(0, 1), (1, 2), (1, 3), (3, 4)]
    for a, b in links:
        (x1, y1), (x2, y2) = consts[a], consts[b]
        body.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{RUST}" stroke-width="4" opacity="0.55"/>')
    for x, y in consts[1:]:
        body.append(f'<circle cx="{x}" cy="{y}" r="11" fill="{EMBER}" opacity="0.75"/>')
    # 좌상단 희미한 육각 결정
    hx, hy, hr = 300, 300, 150
    pts = " ".join(
        f"{hx + hr * math.cos(math.radians(60 * i - 90)):.0f},{hy + hr * math.sin(math.radians(60 * i - 90)):.0f}"
        for i in range(6)
    )
    body.append(f'<polygon points="{pts}" fill="none" stroke="{FAINT}" stroke-width="4" opacity="0.5"/>')
    return "".join(body)


def slide3():
    journals = load("journals")
    research = load("research")
    conferences = load("conferences")
    projects = load("projects")

    years = {}
    for p in journals:
        y = int(str(p.get("year", 0))[:4] or 0)
        if y:
            years[y] = years.get(y, 0) + 1
    y_min, y_max = min(years), max(years)
    n = y_max - y_min + 1
    peak = max(years.values())

    body = []
    # 상단: 실제 논문 제목 텍스처 (최신순)
    titles = [str(p.get("title", "")) for p in reversed(journals)]
    rows = [" · ".join(titles[i::3])[:400] for i in range(3)]
    for i, row in enumerate(rows):
        body.append(
            f'<text x="40" y="{86 + i * 58}" font-family="{FONT}" font-size="30" '
            f'fill="{FAINT}" opacity="{0.5 - 0.1 * i}">{row.replace("&", "&amp;").replace("<", "&lt;")}</text>'
        )
    # 하단: 연도별 논문 막대 (데이터 기반 — 논문 추가 시 자동 갱신)
    margin, base = 150, 1450
    bw = (W - 2 * margin) / n * 0.62
    for y in range(y_min, y_max + 1):
        c = years.get(y, 0)
        if not c:
            continue
        x = margin + (y - y_min) / (n - 1) * (W - 2 * margin) - bw / 2
        h = 60 + (c / peak) * 300
        body.append(
            f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{bw:.0f}" height="{h:.0f}" rx="8" '
            f'fill="url(#bar)" opacity="0.9"/>'
            f'<rect x="{x:.0f}" y="{base - h:.0f}" width="{bw:.0f}" height="6" rx="3" fill="{EMBER}"/>'
        )
        if y % 5 == 0 or y == y_max:
            body.append(
                f'<text x="{x + bw / 2:.0f}" y="1502" font-family="{FONT}" font-size="28" '
                f'fill="{MUTED}" opacity="0.8" text-anchor="middle">{y}</text>'
            )
    # 우상단: 실적 스탯 (데이터 기반)
    stats = [
        (len(journals), "JOURNAL ARTICLES"),
        (len(conferences), "CONFERENCE TALKS"),
        (len(projects), "RESEARCH PROJECTS"),
        (len(research), "RESEARCH AREAS"),
    ]
    for i, (num, label) in enumerate(stats):
        yy = 320 + i * 92
        body.append(
            f'<text x="2160" y="{yy}" font-family="{FONT}" font-size="64" font-weight="700" '
            f'fill="{EMBER}" text-anchor="end" opacity="0.95">{num}</text>'
            f'<text x="2195" y="{yy}" font-family="{FONT}" font-size="26" letter-spacing="4" '
            f'fill="{MUTED}" opacity="0.8">{label}</text>'
        )
    return "".join(body)


CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def main():
    slides = {"slide1": slide1(), "slide2": slide2(), "slide3": slide3()}
    for name, body in slides.items():
        path = svg(name, body)
        png = WORK / f"{name}.png"
        png.unlink(missing_ok=True)
        subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
             f"--screenshot={png}", f"--window-size={W},{H}", path.as_uri()],
            check=True, capture_output=True,
        )
        if not png.exists():
            sys.exit(f"render failed: {name}")
        target = OUT / f"{name}.png"
        target.write_bytes(png.read_bytes())
        print(f"OK {target}")


if __name__ == "__main__":
    main()
