#!/usr/bin/env python3
"""Build Quiet Harbor Props: original code-drawn SVG/PNG icons, cover, screenshots, zip.

No AI images, no stock images, no third-party trademarks.
Cover typography uses SIL Open Font License faces already on this machine
(Alegreya, Albert Sans). Font files are not bundled in the download zip.
"""
from __future__ import annotations

import subprocess
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent.parent  # project root (edit as needed)
PRODUCT = ROOT / "product"
WORK = ROOT / "build-work"
SRC_SVG = WORK / "svg"

# Palette — original, documented in README
INK = "#1E2A3A"
NAVY = "#243656"
SEA = "#2F6A6A"
SEA_DK = "#1F4E50"
FOAM = "#A9C7C2"
PAPER = "#F4E6C8"
AMBER = "#E6A23C"
FLAME = "#F3C56B"
GLOW = "#F8E2A4"
RUST = "#C46B4A"
ROPE = "#B8956A"
CREAM = "#FBF6EC"
WOOD = "#8B5E3C"
WOOD_DK = "#5C3A22"
WHITE = "#F7F1E6"
TEAL = "#3E8A82"
SKY = "#4A6A8A"

ALEGREYA = "/usr/share/fonts/truetype/sand-box/google/Alegreya/Alegreya-VariableFont_wght.ttf"
ALBERT = "/usr/share/fonts/truetype/sand-box/google/Albert Sans/AlbertSans-VariableFont_wght.ttf"
PLEX = "/usr/share/fonts/truetype/sand-box/google/IBM Plex Sans/IBMPlexSans-VariableFont_wdth,wght.ttf"

SW = 6  # consistent stroke


def font(path: str, size: int, weight: int = 400, width: int | None = None) -> ImageFont.FreeTypeFont:
    f = ImageFont.truetype(path, size)
    try:
        if width is not None:
            f.set_variation_by_axes([width, weight])
        else:
            f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f


def doc(body: str, w: int = 256, h: int = 256) -> str:
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" fill="none">\n'
        f"  {body.strip()}\n"
        "</svg>\n"
    )


def st(color: str = INK, w: float = SW, fill: str = "none") -> str:
    return (
        f'stroke="{color}" stroke-width="{w}" stroke-linecap="round" '
        f'stroke-linejoin="round" fill="{fill}"'
    )


# ---------- icons ----------

def icon_paper_lantern() -> str:
    return f"""
  <ellipse cx="128" cy="142" rx="48" ry="62" {st(INK, SW, PAPER)} />
  <ellipse cx="128" cy="142" rx="34" ry="50" {st(AMBER, 3, "none")} />
  <path d="M96 92 C96 78 160 78 160 92" {st(INK, SW, WOOD)} />
  <rect x="108" y="78" width="40" height="16" rx="3" {st(INK, 5, WOOD_DK)} />
  <path d="M128 78 V58" {st(INK, 5)} />
  <path d="M118 58 H138" {st(INK, 5)} />
  <path d="M128 204 V222" {st(ROPE, 4)} />
  <circle cx="128" cy="228" r="6" {st(RUST, 3, RUST)} />
  <path d="M128 128 C122 128 118 136 128 148 C138 136 134 128 128 128 Z" {st(AMBER, 2, FLAME)} />
"""


def icon_lantern_cluster() -> str:
    return f"""
  <path d="M40 64 H216" {st(INK, 5)} />
  <path d="M72 64 V88" {st(ROPE, 4)} />
  <path d="M128 64 V80" {st(ROPE, 4)} />
  <path d="M184 64 V100" {st(ROPE, 4)} />
  <ellipse cx="72" cy="122" rx="22" ry="30" {st(INK, 5, PAPER)} />
  <rect x="62" y="88" width="20" height="10" rx="2" {st(INK, 4, WOOD)} />
  <path d="M72 152 V164" {st(ROPE, 3)} />
  <ellipse cx="128" cy="126" rx="28" ry="38" {st(INK, 5, AMBER)} />
  <rect x="116" y="80" width="24" height="12" rx="2" {st(INK, 4, WOOD_DK)} />
  <path d="M128 164 V180" {st(ROPE, 3)} />
  <ellipse cx="184" cy="140" rx="20" ry="28" {st(INK, 5, RUST)} />
  <rect x="174" y="100" width="20" height="10" rx="2" {st(INK, 4, WOOD)} />
  <path d="M184 168 V180" {st(ROPE, 3)} />
"""


def icon_lamp_post() -> str:
    return f"""
  <path d="M88 232 H128" {st(INK, 8)} />
  <path d="M108 232 V86" {st(INK, 8, NAVY)} />
  <path d="M108 86 C108 70 168 70 168 92" {st(INK, 6, "none")} />
  <path d="M168 92 V110" {st(INK, 5)} />
  <ellipse cx="168" cy="148" rx="28" ry="36" {st(INK, 5, FLAME)} />
  <rect x="156" y="110" width="24" height="12" rx="2" {st(INK, 4, WOOD_DK)} />
  <path d="M168 184 V196" {st(ROPE, 3)} />
  <circle cx="168" cy="202" r="4" {st(RUST, 3, RUST)} />
  <path d="M168 136 C164 136 162 142 168 150 C174 142 172 136 168 136 Z" {st(AMBER, 2, GLOW)} />
"""


def icon_buoy() -> str:
    return f"""
  <path d="M128 48 V78" {st(INK, 5)} />
  <circle cx="128" cy="48" r="8" {st(INK, 4, "none")} />
  <ellipse cx="128" cy="150" rx="44" ry="70" {st(INK, SW, RUST)} />
  <path d="M86 128 H170" {st(INK, 0, WHITE)} />
  <rect x="86" y="118" width="84" height="28" {st("none", 0, WHITE)} />
  <path d="M86 118 C86 118 128 112 170 118 V146 C128 140 86 146 86 146 Z" {st(INK, 4, WHITE)} />
  <ellipse cx="128" cy="150" rx="44" ry="70" {st(INK, SW, "none")} />
  <path d="M128 220 V236" {st(INK, 4)} />
  <circle cx="128" cy="240" r="5" {st(INK, 3, "none")} />
"""


def icon_crate() -> str:
    return f"""
  <rect x="56" y="72" width="144" height="128" rx="4" {st(INK, SW, WOOD)} />
  <path d="M56 104 H200" {st(INK, 5)} />
  <path d="M56 136 H200" {st(INK, 5)} />
  <path d="M56 168 H200" {st(INK, 5)} />
  <path d="M92 72 V200" {st(INK, 5)} />
  <path d="M164 72 V200" {st(INK, 5)} />
  <rect x="56" y="72" width="144" height="128" rx="4" {st(INK, SW, "none")} />
  <path d="M76 84 L88 96 M180 84 L168 96" {st(WOOD_DK, 4)} />
"""


def icon_bollard() -> str:
    return f"""
  <path d="M64 220 H192" {st(SEA, 8)} />
  <path d="M72 220 Q128 236 184 220" {st(FOAM, 4)} />
  <rect x="96" y="88" width="64" height="132" rx="8" {st(INK, SW, NAVY)} />
  <rect x="88" y="72" width="80" height="28" rx="10" {st(INK, SW, INK)} />
  <circle cx="168" cy="86" r="10" {st(INK, 4, "none")} />
  <path d="M176 86 Q210 86 210 130" {st(ROPE, 5)} />
  <path d="M210 130 Q210 150 188 150" {st(ROPE, 5)} />
"""


def icon_coiled_rope() -> str:
    return f"""
  <ellipse cx="128" cy="128" rx="78" ry="78" {st(ROPE, 10, "none")} />
  <ellipse cx="128" cy="128" rx="58" ry="58" {st(WOOD, 10, "none")} />
  <ellipse cx="128" cy="128" rx="38" ry="38" {st(ROPE, 10, "none")} />
  <ellipse cx="128" cy="128" rx="20" ry="20" {st(WOOD, 10, "none")} />
  <circle cx="128" cy="128" r="6" {st(INK, 3, WOOD_DK)} />
  <path d="M206 128 C230 128 230 86 200 78" {st(ROPE, 10)} />
  <path d="M200 78 L214 62" {st(ROPE, 8)} />
"""


def icon_rowboat() -> str:
    return f"""
  <path d="M36 150 C60 196 196 196 220 150 L200 126 L56 126 Z" {st(INK, SW, WOOD)} />
  <path d="M64 126 V150 M128 126 V168 M192 126 V150" {st(INK, 5)} />
  <path d="M56 126 H200" {st(INK, 5)} />
  <path d="M40 168 C80 184 176 184 216 168" {st(SEA, 5)} />
  <path d="M28 184 C80 198 176 198 228 184" {st(FOAM, 4)} />
  <path d="M84 118 L48 78" {st(WOOD_DK, 6)} />
  <path d="M36 70 L60 86 L40 90 Z" {st(INK, 4, WOOD)} />
"""


def icon_ticket_stub() -> str:
    return f"""
  <path d="M48 88 H152 C152 88 152 104 168 104 C184 104 184 88 184 88 H208 V168 H184 C184 168 184 152 168 152 C152 152 152 168 152 168 H48 Z"
        {st(INK, SW, PAPER)} />
  <path d="M152 88 V168" {st(INK, 3)} stroke-dasharray="6 8" />
  <circle cx="80" cy="112" r="8" {st(INK, 3, "none")} />
  <path d="M100 108 H140 M100 122 H128" {st(AMBER, 5)} />
  <path d="M64 144 H140" {st(SEA, 4)} />
"""


def icon_anchor() -> str:
    return f"""
  <circle cx="128" cy="64" r="16" {st(INK, SW, "none")} />
  <path d="M128 80 V200" {st(INK, 8)} />
  <path d="M96 112 H160" {st(INK, 8)} />
  <path d="M128 200 C128 200 56 184 56 136" {st(INK, 8)} />
  <path d="M128 200 C128 200 200 184 200 136" {st(INK, 8)} />
  <path d="M56 136 L44 120 M56 136 L72 124" {st(INK, 7)} />
  <path d="M200 136 L212 120 M200 136 L188 124" {st(INK, 7)} />
  <circle cx="128" cy="64" r="6" {st(INK, 3, "none")} />
"""


def icon_fish_basket() -> str:
    return f"""
  <path d="M72 96 C72 96 128 72 184 96 L196 196 H60 Z" {st(INK, SW, ROPE)} />
  <path d="M80 124 H176 M76 152 H180 M72 180 H184" {st(WOOD_DK, 4)} />
  <path d="M96 96 V196 M128 88 V196 M160 96 V196" {st(WOOD_DK, 4)} />
  <path d="M72 96 C72 96 128 72 184 96" {st(INK, 6)} />
  <path d="M88 96 C88 70 168 70 168 96" {st(INK, 5)} />
  <ellipse cx="110" cy="86" rx="16" ry="8" {st(INK, 4, TEAL)} />
  <path d="M96 86 L88 76 L96 80" {st(INK, 3, TEAL)} />
  <ellipse cx="150" cy="82" rx="16" ry="8" {st(INK, 4, SEA)} />
  <path d="M164 82 L176 72 L166 78" {st(INK, 3, SEA)} />
"""


def icon_tide_gauge() -> str:
    return f"""
  <rect x="108" y="40" width="40" height="176" rx="4" {st(INK, SW, WOOD)} />
  <path d="M116 70 H140 M116 100 H140 M116 130 H132 M116 160 H140 M116 190 H132" {st(INK, 4)} />
  <path d="M40 154 H216" {st(SEA, 6)} />
  <path d="M40 168 C70 160 90 176 128 168 C166 160 186 176 216 168" {st(FOAM, 4)} />
  <path d="M40 184 C80 174 100 190 128 182 C156 174 176 190 216 182" {st(SEA, 4)} />
"""


def icon_lighthouse() -> str:
    return f"""
  <path d="M96 220 L110 96 H146 L160 220 Z" {st(INK, SW, WHITE)} />
  <path d="M110 140 H146 L148 164 H108 Z" {st(INK, 3, RUST)} />
  <rect x="100" y="76" width="56" height="22" rx="2" {st(INK, 5, NAVY)} />
  <polygon points="128,44 140,76 116,76" {st(INK, 5, RUST)} />
  <circle cx="128" cy="86" r="6" {st(AMBER, 2, FLAME)} />
  <path d="M148 86 L210 64 M148 90 L210 90 M148 94 L210 116" {st(FLAME, 4)} />
  <path d="M108 86 L46 64 M108 90 L46 90 M108 94 L46 116" {st(FLAME, 4)} />
  <path d="M80 220 H176" {st(INK, 8)} />
  <rect x="118" y="176" width="20" height="28" rx="2" {st(INK, 3, NAVY)} />
"""


def icon_seagull() -> str:
    return f"""
  <path d="M36 160 C84 108 112 108 128 148 C144 108 172 108 220 160" {st(INK, 8)} />
  <path d="M128 148 C128 148 134 132 128 118" {st(INK, 5)} />
  <circle cx="124" cy="116" r="3" {st(INK, 2, INK)} />
"""


def icon_wave() -> str:
    return f"""
  <path d="M28 168 C52 168 60 120 92 120 C124 120 124 168 160 168 C196 168 196 120 228 128"
        {st(SEA, 8)} />
  <path d="M28 196 C60 196 68 156 104 156 C140 156 140 196 176 196 C212 196 216 164 228 168"
        {st(FOAM, 6)} />
  <path d="M36 216 C80 208 100 224 140 216 C180 208 200 224 228 216" {st(SEA_DK, 5)} />
"""


def icon_dock_piling() -> str:
    return f"""
  <rect x="64" y="72" width="32" height="140" rx="4" {st(INK, SW, WOOD_DK)} />
  <rect x="160" y="88" width="32" height="124" rx="4" {st(INK, SW, WOOD_DK)} />
  <rect x="48" y="120" width="160" height="28" rx="3" {st(INK, SW, WOOD)} />
  <path d="M56 134 H200" {st(WOOD_DK, 3)} />
  <path d="M40 212 C80 200 120 220 160 208 C190 200 210 214 224 208" {st(SEA, 5)} />
  <path d="M80 72 V56 M176 88 V68" {st(ROPE, 4)} />
  <path d="M72 56 H88 M168 68 H184" {st(ROPE, 4)} />
"""


def icon_lantern_reflection() -> str:
    return f"""
  <ellipse cx="128" cy="96" rx="30" ry="40" {st(INK, 5, AMBER)} />
  <rect x="114" y="54" width="28" height="12" rx="2" {st(INK, 4, WOOD_DK)} />
  <path d="M128 54 V42" {st(INK, 4)} />
  <path d="M128 136 V146" {st(ROPE, 3)} />
  <circle cx="128" cy="152" r="4" {st(RUST, 3, RUST)} />
  <path d="M40 168 H216" {st(SEA, 5)} />
  <path d="M128 178 V188" {st(FLAME, 7)} />
  <path d="M128 198 V206" {st(FLAME, 5)} />
  <path d="M128 216 V222" {st(GLOW, 4)} />
"""


def icon_barrel() -> str:
    return f"""
  <path d="M80 68 C80 52 176 52 176 68 V188 C176 204 80 204 80 188 Z" {st(INK, SW, WOOD)} />
  <path d="M78 92 H178" {st(INK, 6)} />
  <path d="M76 128 H180" {st(INK, 7)} />
  <path d="M78 164 H178" {st(INK, 6)} />
  <path d="M96 68 V188 M160 68 V188" {st(WOOD_DK, 4)} />
  <ellipse cx="128" cy="68" rx="48" ry="14" {st(INK, 5, WOOD_DK)} />
"""


def icon_life_ring() -> str:
    return f"""
  <circle cx="128" cy="128" r="70" {st(INK, 14, "none")} />
  <circle cx="128" cy="128" r="70" {st(WHITE, 10, "none")} />
  <circle cx="128" cy="128" r="42" {st(INK, 6, "none")} />
  <path d="M128 58 V86 M128 170 V198 M58 128 H86 M170 128 H198" {st(RUST, 14)} />
  <circle cx="128" cy="128" r="70" {st(INK, 6, "none")} />
  <path d="M96 72 L80 52 M160 72 L176 52 M96 184 L80 204 M160 184 L176 204" {st(ROPE, 5)} />
"""


def icon_harbor_bell() -> str:
    return f"""
  <path d="M72 64 H184" {st(INK, 8)} />
  <path d="M100 64 V84 H156 V64" {st(INK, 6)} />
  <path d="M100 92 L84 160 C84 176 104 188 128 188 C152 188 172 176 172 160 L156 92 Z"
        {st(INK, SW, AMBER)} />
  <rect x="108" y="80" width="40" height="18" rx="3" {st(INK, 5, WOOD_DK)} />
  <circle cx="128" cy="200" r="8" {st(INK, 4, RUST)} />
  <path d="M128 208 V228" {st(ROPE, 4)} />
  <path d="M128 228 C128 228 110 236 110 222" {st(ROPE, 4)} />
"""


def icon_signboard() -> str:
    return f"""
  <rect x="116" y="40" width="24" height="180" rx="3" {st(INK, SW, WOOD_DK)} />
  <rect x="52" y="72" width="152" height="96" rx="6" {st(INK, SW, WOOD)} />
  <rect x="64" y="84" width="128" height="72" rx="4" {st(INK, 4, PAPER)} />
  <path d="M128 100 C124 100 120 108 128 118 C136 108 132 100 128 100 Z" {st(AMBER, 2, FLAME)} />
  <path d="M114 122 H142 M120 134 H136" {st(SEA, 4)} />
  <path d="M96 220 H160" {st(INK, 8)} />
"""


def icon_hanging_fish() -> str:
    return f"""
  <path d="M48 64 H208" {st(INK, 5)} />
  <path d="M88 64 V100" {st(ROPE, 4)} />
  <path d="M168 64 V112" {st(ROPE, 4)} />
  <ellipse cx="88" cy="128" rx="28" ry="16" {st(INK, 5, TEAL)} />
  <path d="M60 128 L40 112 L48 128 L40 144 Z" {st(INK, 4, TEAL)} />
  <circle cx="104" cy="124" r="3" {st(INK, 2, INK)} />
  <ellipse cx="168" cy="140" rx="30" ry="16" {st(INK, 5, SEA)} />
  <path d="M198 140 L220 122 L210 140 L220 158 Z" {st(INK, 4, SEA)} />
  <circle cx="150" cy="136" r="3" {st(INK, 2, INK)} />
"""


def icon_cargo_net() -> str:
    return f"""
  <path d="M80 56 C80 56 128 40 176 56 L200 200 H56 Z" {st(INK, 5, "none")} />
  <path d="M80 56 C80 56 128 40 176 56" {st(INK, 6)} />
  <path d="M88 56 C88 40 168 40 168 56" {st(ROPE, 5)} />
  <path d="M92 88 H172 M84 120 H180 M76 152 H184 M68 184 H188" {st(ROPE, 3)} />
  <path d="M96 64 V200 M128 52 V200 M160 64 V200" {st(ROPE, 3)} />
  <circle cx="128" cy="140" r="16" {st(INK, 4, RUST)} />
  <rect x="108" y="160" width="40" height="24" rx="3" {st(INK, 4, WOOD)} />
"""


def icon_map_scroll() -> str:
    return f"""
  <path d="M60 72 H196 V184 H60 Z" {st(INK, SW, PAPER)} />
  <ellipse cx="60" cy="128" rx="16" ry="56" {st(INK, 5, ROPE)} />
  <ellipse cx="196" cy="128" rx="16" ry="56" {st(INK, 5, ROPE)} />
  <path d="M88 128 C108 116 120 140 140 128 C160 116 172 136 180 128" {st(SEA, 5)} />
  <circle cx="120" cy="108" r="5" {st(RUST, 2, RUST)} />
  <path d="M96 156 H168" {st(WOOD, 3)} stroke-dasharray="6 6" />
"""


def icon_compass_rose() -> str:
    return f"""
  <circle cx="128" cy="128" r="84" {st(INK, 5, CREAM)} />
  <circle cx="128" cy="128" r="68" {st(SEA, 2, "none")} />
  <polygon points="128,40 140,128 128,128 116,128" {st(INK, 3, RUST)} />
  <polygon points="128,216 140,128 116,128" {st(INK, 3, NAVY)} />
  <polygon points="40,128 128,116 128,140" {st(INK, 3, NAVY)} />
  <polygon points="216,128 128,116 128,140" {st(INK, 3, NAVY)} />
  <polygon points="70,70 128,120 128,128 120,128" {st(INK, 3, AMBER)} />
  <polygon points="186,70 128,120 128,128 136,128" {st(INK, 3, AMBER)} />
  <polygon points="70,186 128,136 128,128 120,128" {st(INK, 3, AMBER)} />
  <polygon points="186,186 128,136 128,128 136,128" {st(INK, 3, AMBER)} />
  <circle cx="128" cy="128" r="10" {st(INK, 4, FLAME)} />
  <path d="M128 28 V40 M128 216 V228 M28 128 H40 M216 128 H228" {st(INK, 4)} />
"""


def icon_gangplank() -> str:
    return f"""
  <path d="M36 84 L220 172 L208 196 L24 108 Z" {st(INK, SW, WOOD)} />
  <path d="M52 100 L196 168 M68 116 L180 168" {st(WOOD_DK, 4)} />
  <path d="M48 76 L232 160" {st(ROPE, 5)} />
  <path d="M24 112 L208 204" {st(ROPE, 5)} />
  <path d="M48 76 L36 84 M24 112 L24 108" {st(ROPE, 5)} />
  <rect x="200" y="148" width="24" height="64" rx="3" {st(INK, 5, WOOD_DK)} />
"""


def icon_glowing_window() -> str:
    return f"""
  <rect x="56" y="40" width="144" height="180" rx="4" {st(INK, SW, NAVY)} />
  <rect x="80" y="72" width="96" height="80" rx="3" {st(INK, 5, FLAME)} />
  <path d="M128 72 V152 M80 112 H176" {st(INK, 6)} />
  <rect x="96" y="172" width="28" height="48" rx="2" {st(INK, 4, WOOD_DK)} />
  <path d="M64 40 H192 L184 28 H72 Z" {st(INK, 5, RUST)} />
  <circle cx="118" cy="196" r="3" {st(AMBER, 2, AMBER)} />
"""


def icon_oar() -> str:
    return f"""
  <path d="M60 200 L170 72" {st(WOOD, 12)} />
  <path d="M60 200 L170 72" {st(INK, 4)} />
  <path d="M154 52 C190 36 214 72 190 100 C170 84 160 70 154 52 Z" {st(INK, SW, WOOD_DK)} />
  <path d="M52 208 C44 220 56 228 68 216" {st(INK, 5)} />
"""


def icon_starfish() -> str:
    return f"""
  <polygon points="128,44 144,104 208,104 156,142 176,204 128,166 80,204 100,142 48,104 112,104"
           {st(INK, SW, RUST)} />
  <circle cx="128" cy="128" r="14" {st(INK, 3, PAPER)} />
  <path d="M36 208 C80 196 140 216 220 200" {st(FOAM, 4)} />
"""


def icon_lantern_string() -> str:
    return f"""
  <path d="M28 72 Q128 40 228 72" {st(INK, 5)} />
  <path d="M56 64 V88 M92 56 V84 M128 52 V80 M164 56 V84 M200 64 V88" {st(ROPE, 3)} />
  <ellipse cx="56" cy="108" rx="14" ry="18" {st(INK, 4, PAPER)} />
  <ellipse cx="92" cy="106" rx="14" ry="18" {st(INK, 4, AMBER)} />
  <ellipse cx="128" cy="104" rx="16" ry="22" {st(INK, 4, RUST)} />
  <ellipse cx="164" cy="106" rx="14" ry="18" {st(INK, 4, FLAME)} />
  <ellipse cx="200" cy="108" rx="14" ry="18" {st(INK, 4, TEAL)} />
  <rect x="50" y="84" width="12" height="8" rx="1" {st(INK, 3, WOOD)} />
  <rect x="86" y="80" width="12" height="8" rx="1" {st(INK, 3, WOOD)} />
  <rect x="121" y="76" width="14" height="8" rx="1" {st(INK, 3, WOOD_DK)} />
  <rect x="158" y="80" width="12" height="8" rx="1" {st(INK, 3, WOOD)} />
  <rect x="194" y="84" width="12" height="8" rx="1" {st(INK, 3, WOOD)} />
"""


def icon_moon_over_water() -> str:
    return f"""
  <circle cx="128" cy="88" r="44" {st(INK, 5, PAPER)} />
  <circle cx="114" cy="80" r="8" {st(INK, 2, "#E8D7B0")} />
  <circle cx="142" cy="100" r="12" {st(INK, 2, "#E8D7B0")} />
  <circle cx="122" cy="108" r="5" {st(INK, 2, "#E8D7B0")} />
  <path d="M32 176 H224" {st(SEA, 5)} />
  <path d="M128 184 V190" {st(GLOW, 7)} />
  <path d="M118 202 H138" {st(GLOW, 6)} />
  <path d="M110 218 H146" {st(FLAME, 5)} />
  <path d="M40 200 C80 190 100 210 128 200 C156 190 176 210 216 200" {st(FOAM, 4)} />
"""


def icon_mooring_cleat() -> str:
    return f"""
  <rect x="40" y="176" width="176" height="36" rx="4" {st(INK, SW, WOOD)} />
  <path d="M56 194 H200" {st(WOOD_DK, 3)} />
  <path d="M88 176 V120 H168 V176" {st(INK, 8, NAVY)} />
  <rect x="64" y="108" width="128" height="28" rx="12" {st(INK, SW, INK)} />
  <path d="M72 122 C40 90 40 60 80 56" {st(ROPE, 8)} />
  <path d="M80 56 C120 52 140 80 128 108" {st(ROPE, 8)} />
  <path d="M184 122 C220 96 216 56 176 64" {st(ROPE, 8)} />
"""


ICONS = [
    ("01-paper-lantern", "Paper lantern", icon_paper_lantern),
    ("02-lantern-cluster", "Lantern cluster", icon_lantern_cluster),
    ("03-lamp-post", "Harbor lamp post", icon_lamp_post),
    ("04-buoy", "Channel buoy", icon_buoy),
    ("05-crate", "Wooden crate", icon_crate),
    ("06-bollard", "Mooring bollard", icon_bollard),
    ("07-coiled-rope", "Coiled rope", icon_coiled_rope),
    ("08-rowboat", "Rowboat", icon_rowboat),
    ("09-ticket-stub", "Ferry ticket stub", icon_ticket_stub),
    ("10-anchor", "Anchor", icon_anchor),
    ("11-fish-basket", "Fish basket", icon_fish_basket),
    ("12-tide-gauge", "Tide gauge", icon_tide_gauge),
    ("13-lighthouse", "Lighthouse", icon_lighthouse),
    ("14-seagull", "Seagull", icon_seagull),
    ("15-wave", "Waves", icon_wave),
    ("16-dock-piling", "Dock pilings", icon_dock_piling),
    ("17-lantern-reflection", "Lantern reflection", icon_lantern_reflection),
    ("18-barrel", "Cargo barrel", icon_barrel),
    ("19-life-ring", "Life ring", icon_life_ring),
    ("20-harbor-bell", "Harbor bell", icon_harbor_bell),
    ("21-signboard", "Blank signboard", icon_signboard),
    ("22-hanging-fish", "Hanging fish", icon_hanging_fish),
    ("23-cargo-net", "Cargo net", icon_cargo_net),
    ("24-map-scroll", "Harbor chart scroll", icon_map_scroll),
    ("25-compass-rose", "Compass rose", icon_compass_rose),
    ("26-gangplank", "Gangplank", icon_gangplank),
    ("27-glowing-window", "Glowing window", icon_glowing_window),
    ("28-oar", "Oar", icon_oar),
    ("29-starfish", "Starfish", icon_starfish),
    ("30-lantern-string", "Lantern string", icon_lantern_string),
    ("31-moon-over-water", "Moon over water", icon_moon_over_water),
    ("32-mooring-cleat", "Mooring cleat", icon_mooring_cleat),
]


README = """Quiet Harbor Props
Version 1.0.0
Publisher: Lanternbay Studio
https://csvclinic.itch.io  (project page published after upload)

What this is
------------
A 32-piece vector prop pack for 2D games, visual novels, maps, and UI
decoration. Every icon is original line-and-fill art drawn in code
(SVG paths). There are no AI-generated images, no stock photos, and
no third-party logos or trademarks.

Contents
--------
  svg/           32 standalone SVG files (256 viewBox, scalable)
  png/256/       32 PNG exports, 256 x 256 px
  png/512/       32 PNG exports, 512 x 512 px
  sheets/        Contact sheet of all 32 icons
  LICENSE.txt    Terms of use
  README.txt     This file
  source/        The Python script that drew the icons

Icon list
---------
  01 paper lantern          02 lantern cluster
  03 harbor lamp post       04 channel buoy
  05 wooden crate           06 mooring bollard
  07 coiled rope            08 rowboat
  09 ferry ticket stub      10 anchor
  11 fish basket            12 tide gauge
  13 lighthouse             14 seagull
  15 waves                  16 dock pilings
  17 lantern reflection     18 cargo barrel
  19 life ring              20 harbor bell
  21 blank signboard        22 hanging fish
  23 cargo net              24 harbor chart scroll
  25 compass rose           26 gangplank
  27 glowing window         28 oar
  29 starfish               30 lantern string
  31 moon over water        32 mooring cleat

Color palette (hex)
-------------------
  Ink #1E2A3A    Navy #243656    Sea #2F6A6A    Foam #A9C7C2
  Paper #F4E6C8  Amber #E6A23C   Flame #F3C56B  Glow #F8E2A4
  Rust #C46B4A   Rope #B8956A    Wood #8B5E3C   Cream #FBF6EC

How to use
----------
Drop the SVG files into a vector tool or game engine, or use the PNG
exports as sprites or UI icons. You may recolor and adapt them. See
LICENSE.txt for credit and redistribution rules.

Credits
-------
Art and packaging: Lanternbay Studio, 2026.
Drawn with original SVG path code; rasterized with librsvg (rsvg-convert).
"""

LICENSE = """Quiet Harbor Props
Copyright 2026 Lanternbay Studio

Permission is granted, free of charge, to use, copy, modify, and
incorporate these assets into commercial or non-commercial games,
applications, videos, streams, educational materials, and other
original works.

Conditions
----------
1. Credit "Lanternbay Studio" in your credits, description, or an
   equivalent notice. A short line such as:

     Harbor props by Lanternbay Studio

   is enough.

2. Do not redistribute the original files, or a lightly modified
   copy, as a standalone asset pack, icon set, or stock collection.

3. Do not claim authorship of the original assets.

4. No trademark rights are granted. The name "Lanternbay Studio"
   remains with the publisher.

5. The assets are provided "as is", without warranty of any kind.

These files are original vector drawings created in code. They do
not include AI-generated images, stock photographs, or third-party
trademarks.
"""


def write_svgs() -> None:
    SRC_SVG.mkdir(parents=True, exist_ok=True)
    for slug, _title, fn in ICONS:
        (SRC_SVG / f"{slug}.svg").write_text(doc(fn()), encoding="utf-8")


def rasterize(svg: Path, png: Path, size: int) -> None:
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["rsvg-convert", "-w", str(size), "-h", str(size), str(svg), "-o", str(png)],
        check=True,
    )


def contact_sheet(png_dir: Path, out: Path, cell: int = 256, pad: int = 24, cols: int = 8) -> Image.Image:
    rows = (len(ICONS) + cols - 1) // cols
    bg = "#F4EDE0"
    w = pad + cols * (cell + pad)
    h = pad + rows * (cell + pad)
    img = Image.new("RGBA", (w, h), bg)
    for i, (slug, _t, _fn) in enumerate(ICONS):
        im = Image.open(png_dir / f"{slug}.png").convert("RGBA")
        im = im.resize((cell, cell), Image.Resampling.LANCZOS)
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = pad + r * (cell + pad)
        # card
        card = Image.new("RGBA", (cell, cell), CREAM)
        img.paste(card, (x, y))
        img.alpha_composite(im, (x, y))
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    return img


def make_cover(png512: Path, out: Path) -> None:
    W, H = 1260, 1000  # 315:250 * 4
    img = Image.new("RGB", (W, H), "#1A2740")
    d = ImageDraw.Draw(img)
    # water band
    d.rectangle((0, 720, W, H), fill="#152032")
    for i, y in enumerate((760, 800, 850, 910)):
        color = "#2F6A6A" if i % 2 == 0 else "#A9C7C2"
        d.arc((-80, y - 40, W + 80, y + 80), 0, 180, fill=color, width=3)
    # soft lantern glow
    glow = Image.new("RGB", (W, H), "#1A2740")
    gd = ImageDraw.Draw(glow)
    gd.ellipse((430, 220, 830, 620), fill="#4A3310")
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    img = Image.blend(img, glow, 0.45)
    d = ImageDraw.Draw(img)

    title_f = font(ALEGREYA, 92, 700)
    sub_f = font(ALBERT, 28, 500)
    brand_f = font(ALBERT, 22, 500)
    small_f = font(ALBERT, 18, 400)

    featured = [
        "01-paper-lantern",
        "13-lighthouse",
        "08-rowboat",
        "03-lamp-post",
        "19-life-ring",
        "04-buoy",
        "20-harbor-bell",
        "30-lantern-string",
    ]
    # title
    title = "Quiet Harbor Props"
    bbox = d.textbbox((0, 0), title, font=title_f)
    tw = bbox[2] - bbox[0]
    d.text(((W - tw) / 2, 70), title, font=title_f, fill="#F4E6C8")
    sub = "32 vector props for 2D games and visual novels"
    bbox = d.textbbox((0, 0), sub, font=sub_f)
    sw = bbox[2] - bbox[0]
    d.text(((W - sw) / 2, 180), sub, font=sub_f, fill="#A9C7C2")

    # featured icons row
    size = 200
    gap = 16
    total = len(featured) // 2 * (size + gap) - gap
    # two rows of 4
    row_icons = [featured[:4], featured[4:]]
    start_y = 250
    for r, slugs in enumerate(row_icons):
        total = len(slugs) * (size + gap) - gap
        x0 = (W - total) // 2
        for i, slug in enumerate(slugs):
            im = Image.open(png512 / f"{slug}.png").convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
            x = x0 + i * (size + gap)
            y = start_y + r * (size + 20)
            card = Image.new("RGBA", (size, size), "#FBF6EC")
            img.paste(card.convert("RGB"), (x, y))
            tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            tmp.paste(im, (x, y), im)
            img = Image.alpha_composite(img.convert("RGBA"), tmp).convert("RGB")
            d = ImageDraw.Draw(img)

    brand = "LANTERNBAY STUDIO"
    bbox = d.textbbox((0, 0), brand, font=brand_f)
    bw = bbox[2] - bbox[0]
    d.text(((W - bw) / 2, 920), brand, font=brand_f, fill="#E6A23C")
    note = "Original code-drawn SVG + PNG   ·   Free to use with credit"
    bbox = d.textbbox((0, 0), note, font=small_f)
    nw = bbox[2] - bbox[0]
    d.text(((W - nw) / 2, 952), note, font=small_f, fill="#A9C7C2")
    img.save(out, "JPEG", quality=92, optimize=True)


def make_screenshots(png256: Path, png512: Path, sheet: Path, outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)

    # 01 icon sheet with caption
    base = Image.open(sheet).convert("RGB")
    W, H = 1600, 1100
    canvas = Image.new("RGB", (W, H), "#F4EDE0")
    d = ImageDraw.Draw(canvas)
    title_f = font(ALEGREYA, 54, 700)
    sub_f = font(ALBERT, 22, 500)
    d.text((60, 36), "Quiet Harbor Props", font=title_f, fill=INK)
    d.text((60, 106), "All 32 icons  ·  SVG and PNG  ·  Lanternbay Studio", font=sub_f, fill=SEA)
    # fit sheet
    margin = 60
    avail_w = W - 2 * margin
    avail_h = H - 170
    ratio = min(avail_w / base.width, avail_h / base.height)
    nw, nh = int(base.width * ratio), int(base.height * ratio)
    resized = base.resize((nw, nh), Image.Resampling.LANCZOS)
    canvas.paste(resized, ((W - nw) // 2, 150))
    canvas.save(outdir / "01-icon-sheet.png", "PNG", optimize=True)

    # 02 light and dark colorways
    W, H = 1600, 900
    canvas = Image.new("RGB", (W, H), "#F4EDE0")
    d = ImageDraw.Draw(canvas)
    d.rectangle((W // 2, 0, W, H), fill="#1A2740")
    title_f = font(ALEGREYA, 44, 700)
    sub_f = font(ALBERT, 20, 500)
    d.text((48, 28), "On paper", font=title_f, fill=INK)
    d.text((W // 2 + 48, 28), "On night water", font=title_f, fill="#F4E6C8")
    d.text((48, 88), "Cream ground, print-friendly", font=sub_f, fill=SEA)
    d.text((W // 2 + 48, 88), "Navy ground, game HUD / VN use", font=sub_f, fill="#A9C7C2")
    picks = [
        "01-paper-lantern",
        "13-lighthouse",
        "08-rowboat",
        "19-life-ring",
        "05-crate",
        "04-buoy",
    ]
    size = 200
    for i, slug in enumerate(picks):
        im = Image.open(png512 / f"{slug}.png").convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        r, c = divmod(i, 3)
        # left
        x = 60 + c * (size + 24)
        y = 160 + r * (size + 40)
        canvas.paste(Image.new("RGB", (size, size), CREAM), (x, y))
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(im, (x, y), im)
        canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")
        # right
        x2 = W // 2 + 60 + c * (size + 24)
        canvas.paste(Image.new("RGB", (size, size), "#152032"), (x2, y))
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(im, (x2, y), im)
        canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")
    canvas.save(outdir / "02-colorways.png", "PNG", optimize=True)

    # 03 mock dusk pier scene
    W, H = 1600, 900
    canvas = Image.new("RGB", (W, H), "#1A2740")
    d = ImageDraw.Draw(canvas)
    # sky gradient
    for y in range(0, 520):
        t = y / 520
        r = int(26 + (80 - 26) * t)
        g = int(39 + (50 - 39) * t)
        b = int(64 + (40 - 64) * t)
        d.line((0, y, W, y), fill=(r, g, b))
    d.rectangle((0, 520, W, H), fill="#152032")
    # pier
    d.rectangle((0, 560, 1100, 640), fill=WOOD)
    d.rectangle((0, 630, 1100, 660), fill=WOOD_DK)
    for x in range(40, 1100, 70):
        d.rectangle((x, 660, x + 22, 820), fill=WOOD_DK)
    # waves
    for i, y in enumerate((700, 760, 830)):
        d.arc((-100, y, W + 100, y + 90), 0, 180, fill=SEA if i % 2 == 0 else FOAM, width=4)
    # moon
    moon = Image.open(png512 / "31-moon-over-water.png").convert("RGBA").resize((280, 280), Image.Resampling.LANCZOS)
    # lighthouse, lamp, crates, etc.
    def paste_icon(slug, x, y, size):
        nonlocal canvas
        im = Image.open(png512 / f"{slug}.png").convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(im, (x, y), im)
        canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")

    # Moon only (top half of the icon, no water line in the sky)
    moon = Image.open(png512 / "31-moon-over-water.png").convert("RGBA").resize((260, 260), Image.Resampling.LANCZOS)
    moon = moon.crop((0, 0, 260, 170))
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tmp.paste(moon, (1260, 30), moon)
    canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")
    # Small rock for the lighthouse
    d = ImageDraw.Draw(canvas)
    d.polygon([(1260, 620), (1320, 560), (1500, 560), (1580, 620), (1560, 680), (1280, 680)], fill="#3A3A48")
    paste_icon("13-lighthouse", 1280, 320, 260)
    paste_icon("03-lamp-post", 40, 270, 300)
    paste_icon("30-lantern-string", 340, 160, 340)
    paste_icon("05-crate", 280, 400, 180)
    paste_icon("18-barrel", 460, 400, 180)
    paste_icon("19-life-ring", 640, 410, 160)
    paste_icon("08-rowboat", 860, 560, 280)
    paste_icon("14-seagull", 780, 80, 200)
    d = ImageDraw.Draw(canvas)
    cap_f = font(ALBERT, 22, 500)
    d.text((48, 840), "Example arrangement  ·  Quiet Harbor Props  ·  Lanternbay Studio", font=cap_f, fill="#F4E6C8")
    canvas.save(outdir / "03-mock-scene.png", "PNG", optimize=True)

    # 04 what's included
    W, H = 1600, 900
    canvas = Image.new("RGB", (W, H), "#F4EDE0")
    d = ImageDraw.Draw(canvas)
    title_f = font(ALEGREYA, 54, 700)
    body_f = font(ALBERT, 28, 400)
    strong_f = font(ALBERT, 28, 600)
    d.text((80, 60), "What's in the pack", font=title_f, fill=INK)
    lines = [
        ("32 original icons", "SVG (scalable) plus PNG at 256 and 512 px"),
        ("Contact sheet", "All icons on one page, ready to browse"),
        ("Source script", "The Python that drew every path, included"),
        ("License", "Use in commercial games; credit Lanternbay Studio"),
        ("No AI, no stock, no logos", "Code-drawn vectors, original palette"),
    ]
    y = 170
    for head, rest in lines:
        d.ellipse((88, y + 10, 108, y + 30), fill=AMBER, outline=INK)
        d.text((130, y), head, font=strong_f, fill=INK)
        d.text((130, y + 40), rest, font=body_f, fill=SEA_DK)
        y += 110
    # side icons
    for i, slug in enumerate(["01-paper-lantern", "25-compass-rose", "10-anchor"]):
        im = Image.open(png512 / f"{slug}.png").convert("RGBA").resize((220, 220), Image.Resampling.LANCZOS)
        x, y = 1260, 140 + i * 230
        canvas.paste(Image.new("RGB", (220, 220), CREAM), (x, y))
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(im, (x, y), im)
        canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")
    canvas.save(outdir / "04-whats-included.png", "PNG", optimize=True)

    # 05 hero close-ups
    W, H = 1600, 900
    canvas = Image.new("RGB", (W, H), "#1A2740")
    d = ImageDraw.Draw(canvas)
    title_f = font(ALEGREYA, 48, 700)
    label_f = font(ALBERT, 20, 500)
    d.text((60, 30), "Hero props, close up", font=title_f, fill="#F4E6C8")
    heroes = [
        ("01-paper-lantern", "Paper lantern"),
        ("13-lighthouse", "Lighthouse"),
        ("08-rowboat", "Rowboat"),
        ("19-life-ring", "Life ring"),
        ("20-harbor-bell", "Harbor bell"),
        ("25-compass-rose", "Compass rose"),
    ]
    size = 340
    for i, (slug, label) in enumerate(heroes):
        r, c = divmod(i, 3)
        x = 80 + c * (size + 80)
        y = 120 + r * (size + 70)
        canvas.paste(Image.new("RGB", (size, size), CREAM), (x, y))
        im = Image.open(png512 / f"{slug}.png").convert("RGBA").resize((size, size), Image.Resampling.LANCZOS)
        tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        tmp.paste(im, (x, y), im)
        canvas = Image.alpha_composite(canvas.convert("RGBA"), tmp).convert("RGB")
        d = ImageDraw.Draw(canvas)
        bbox = d.textbbox((0, 0), label, font=label_f)
        lw = bbox[2] - bbox[0]
        d.text((x + (size - lw) / 2, y + size + 8), label, font=label_f, fill="#A9C7C2")
    canvas.save(outdir / "05-hero-closeups.png", "PNG", optimize=True)


def make_zip(pack_dir: Path, zip_path: Path) -> None:
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(pack_dir.rglob("*")):
            if f.is_file():
                zf.write(f, f.relative_to(pack_dir.parent))


def main() -> None:
    write_svgs()
    pack = WORK / "quiet-harbor-props-1.0.0"
    if pack.exists():
        import shutil
        shutil.rmtree(pack)
    svg_dst = pack / "svg"
    png256 = pack / "png" / "256"
    png512 = pack / "png" / "512"
    sheets = pack / "sheets"
    source = pack / "source"
    svg_dst.mkdir(parents=True)
    png256.mkdir(parents=True)
    png512.mkdir(parents=True)
    sheets.mkdir(parents=True)
    source.mkdir(parents=True)

    for slug, _t, _fn in ICONS:
        src = SRC_SVG / f"{slug}.svg"
        dst = svg_dst / f"{slug}.svg"
        dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        rasterize(src, png256 / f"{slug}.png", 256)
        rasterize(src, png512 / f"{slug}.png", 512)

    contact_sheet(png256, sheets / "icon-sheet.png")
    (pack / "README.txt").write_text(README, encoding="utf-8")
    (pack / "LICENSE.txt").write_text(LICENSE, encoding="utf-8")
    # copy this builder into the pack
    src_self = Path(__file__).resolve()
    if src_self.exists():
        (source / "build_pack.py").write_text(src_self.read_text(encoding="utf-8"), encoding="utf-8")

    PRODUCT.mkdir(parents=True, exist_ok=True)
    shots = PRODUCT / "screenshots"
    make_cover(png512, PRODUCT / "cover.jpg")
    make_screenshots(png256, png512, sheets / "icon-sheet.png", shots)

    zip_path = PRODUCT / "quiet-harbor-props-1.0.0.zip"
    make_zip(pack, zip_path)
    print("Wrote", zip_path, "size", zip_path.stat().st_size)
    print("Cover", PRODUCT / "cover.jpg")
    print("Screenshots", list(shots.glob("*.png")))


if __name__ == "__main__":
    main()
