#!/usr/bin/env python3
"""Generate 5 AIMAP-brand research-area illustrations via OpenAI gpt-image-1."""
import base64
import json
import os
import sys
import urllib.request

KEY = os.environ["OPENAI_API_KEY"]
URL = "https://api.openai.com/v1/images/generations"

STYLE = (
    "Minimalist flat vector-style scientific editorial illustration. "
    "Dark warm charcoal background (#171210) with subtle topographic contour lines, "
    "burnt orange (#D2622B), ember orange (#F0955C) and warm cream (#F4EDE5) as the only accent colors. "
    "Clean geometric shapes, elegant thin line work, premium print-poster aesthetic. "
    "Absolutely no text, no letters, no numbers, no logos, no watermark. Wide landscape composition. "
)

SCENES = {
    "design": "Subject: AI-driven alloy design — a glowing neural network graph morphing into a "
              "polycrystalline metal lattice of hexagonal grains; nodes and edges in orange connect "
              "to atomic crystal structures, suggesting generative design of new metal alloys.",
    "analysis": "Subject: AI-based microstructure analysis — a metal micrograph made of irregular "
                "polygonal grains, half rendered as plain outlines and half filled with orange "
                "segmentation masks, with a thin scanning beam sweeping across, suggesting automated "
                "semantic segmentation of material microstructures.",
    "process": "Subject: physics-informed AI for manufacturing process prediction — a stylized rolling "
               "mill with two rollers pressing a glowing hot metal slab, overlaid with a simulation "
               "mesh grid and smooth flowing field lines, suggesting hybrid physics and machine "
               "learning process simulation.",
    "agent": "Subject: materials-specialized vision-language model and AI agents — a central hexagonal "
             "AI core exchanging beams with floating panels showing a micrograph, a stress-strain "
             "curve and a molecule, connected by circuit-like orange lines, suggesting multimodal "
             "AI agents automating materials research.",
    "autolab": "Subject: autonomous laboratory for metallic materials — a sleek robotic arm placing a "
               "small glowing metal sample onto an automated test stage, surrounded by orbit-like "
               "feedback loop arrows and small instrument silhouettes, suggesting a closed-loop "
               "self-driving laboratory.",
}


def generate(slug: str, scene: str) -> None:
    body = {
        "model": "gpt-image-1",
        "prompt": STYLE + scene,
        "size": "1536x1024",
        "quality": "high",
        "n": 1,
    }
    req = urllib.request.Request(
        URL,
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {KEY}"},
    )
    with urllib.request.urlopen(req, timeout=300) as r:
        resp = json.load(r)
    data = base64.b64decode(resp["data"][0]["b64_json"])
    out = f"img/{slug}.png"
    with open(out, "wb") as f:
        f.write(data)
    print(f"{out}: {len(data)//1024} KB")


os.makedirs("img", exist_ok=True)
targets = sys.argv[1:] or list(SCENES)
for slug in targets:
    try:
        generate(slug, SCENES[slug])
    except urllib.error.HTTPError as e:  # noqa: PERF203
        print(f"{slug}: HTTP {e.code} {e.read().decode()[:300]}")
    except Exception as e:  # noqa: BLE001
        print(f"{slug}: ERROR {e}")
