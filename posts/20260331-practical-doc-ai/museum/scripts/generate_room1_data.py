#!/usr/bin/env python3

from __future__ import annotations

import argparse
import io
import json
import math
import random
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "assets" / "room1"
OUTPUT_DIR = ASSET_DIR / "generated"
TEXTURE_DIR = ASSET_DIR / "textures"
SCALE = 3


def S(value: int | float) -> int:
    return int(round(value * SCALE))


TEMPLATE_SIZE = (S(700), S(1000))
PAGE_BOX = {"x": S(36), "y": S(22), "w": S(628), "h": S(972)}


@dataclass
class Field:
    id: str
    label: str
    value: str
    box: tuple[int, int, int, int]


@dataclass
class CorruptionProfile:
    id: str
    description: str
    print_artifacts: dict[str, Any]
    paper_artifacts: dict[str, Any]
    geometry: dict[str, Any]
    capture: dict[str, Any]


FIELDS = [
    Field("name", "Applicant name", "Alexandra Hayes", (S(110), S(224), S(300), S(30))),
    Field("position", "Position desired", "Senior Operations Analyst", (S(110), S(284), S(250), S(30))),
    Field("address", "Street address", "2714 Red Cedar Lane Larkhaven, TX 78705", (S(110), S(344), S(225), S(56))),
    Field("records_days", "Records due (days)", "15", (S(300), S(889), S(26), S(16))),
]


def load_font(name: str, size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/Library/Fonts") / name,
        Path("/System/Library/Fonts") / name,
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


FONT_TITLE = load_font("Georgia.ttf", S(21))
FONT_SUBTITLE = load_font("Georgia.ttf", S(11))
FONT_LABEL = load_font("Georgia.ttf", S(11))
FONT_VALUE = load_font("Georgia.ttf", S(13))
FONT_VALUE_SMALL = load_font("Georgia.ttf", S(11))
FONT_BODY = load_font("Georgia.ttf", S(10))
FONT_SECTION = load_font("Georgia.ttf", S(10))
FONT_TINY = load_font("Georgia.ttf", S(9))
FONT_MICRO = load_font("Georgia.ttf", S(8))


def ensure_dirs() -> None:
    (OUTPUT_DIR / "variants").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "crops").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "matching").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "textures").mkdir(parents=True, exist_ok=True)


def clear_generated_outputs() -> None:
    for pattern in [
        "variants/*.png",
        "crops/*.png",
        "matching/*.png",
        "template-blank.png",
        "template-filled.png",
        "room1-manifest.json",
    ]:
        for path in OUTPUT_DIR.glob(pattern):
            if path.is_file():
                path.unlink()


def render_template(blank: bool = True, num_history_rows: int = 2, swap_name_position: bool = False) -> Image.Image:
    image = Image.new("RGB", TEMPLATE_SIZE, "#eee3ca")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, TEMPLATE_SIZE[0] - 1, TEMPLATE_SIZE[1] - 1), fill="#eee3ca")
    px, py, pw, ph = PAGE_BOX["x"], PAGE_BOX["y"], PAGE_BOX["w"], PAGE_BOX["h"]
    draw.rectangle((px, py, px + pw, py + ph), fill="#f9f6eb", outline="#9d9278", width=2)

    draw.ellipse((S(94), S(72), S(146), S(124)), fill="#d7ccb4", outline="#8e836a", width=2)
    draw.text((S(164), S(74)), "Employment Application", font=FONT_TITLE, fill="#332b1d")
    draw.text((S(164), S(101)), "Northwind Logistics", font=FONT_SUBTITLE, fill="#5a533f")
    draw.text(
        (S(164), S(121)),
        "Applicant intake form for hourly and salaried roles",
        font=FONT_BODY,
        fill="#5a533f",
    )
    draw.text(
        (S(164), S(136)),
        "Please print clearly. Attach supplemental work history if more space is needed.",
        font=FONT_TINY,
        fill="#6a624d",
    )

    draw.rectangle((S(104), S(164), S(596), S(194)), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((S(116), S(171)), "Section 1. Applicant, Contact, and Role", font=FONT_SECTION, fill="#413828")

    # Repeated semantic fields: names, roles, addresses, and phones.
    # In the revised form, "Position desired" and "Applicant name" swap rows.
    row1_labels = ("Applicant name", "Preferred name / alias")
    row2_labels = ("Position desired", "Department requested")
    if swap_name_position:
        row1_labels, row2_labels = row2_labels, row1_labels

    draw.text((S(110), S(202)), row1_labels[0], font=FONT_LABEL, fill="#574f40")
    draw.text((S(440), S(202)), row1_labels[1], font=FONT_LABEL, fill="#574f40")
    draw.rectangle((S(110), S(224), S(410), S(254)), outline="#756a52", width=1)
    draw.rectangle((S(440), S(224), S(586), S(254)), outline="#756a52", width=1)

    draw.text((S(110), S(262)), row2_labels[0], font=FONT_LABEL, fill="#574f40")
    draw.text((S(390), S(262)), row2_labels[1], font=FONT_LABEL, fill="#574f40")
    draw.rectangle((S(110), S(284), S(360), S(314)), outline="#756a52", width=1)
    draw.rectangle((S(390), S(284), S(586), S(314)), outline="#756a52", width=1)

    draw.text((S(110), S(322)), "Street address", font=FONT_LABEL, fill="#574f40")
    draw.text((S(360), S(322)), "City / State / ZIP", font=FONT_LABEL, fill="#574f40")
    draw.rectangle((S(110), S(344), S(335), S(400)), outline="#756a52", width=1)
    draw.rectangle((S(360), S(344), S(586), S(376)), outline="#756a52", width=1)

    # Reading-order trap: labels across the row, values on the next row.
    contact_labels = [
        ("Mobile phone", S(110)),
        ("Alternate phone", S(255)),
        ("Emergency phone", S(430)),
    ]
    for text, x in contact_labels:
        draw.text((x, S(414)), text, font=FONT_BODY, fill="#6b6557")
    draw.line((S(110), S(448), S(230), S(448)), fill="#b0a58f", width=1)
    draw.line((S(255), S(448), S(405), S(448)), fill="#b0a58f", width=1)
    draw.line((S(430), S(448), S(585), S(448)), fill="#b0a58f", width=1)

    draw.text((S(110), S(458)), "Email address", font=FONT_BODY, fill="#6b6557")
    draw.text((S(345), S(458)), "Current supervisor", font=FONT_BODY, fill="#6b6557")
    draw.line((S(110), S(486), S(320), S(486)), fill="#b0a58f", width=1)
    draw.line((S(345), S(486), S(586), S(486)), fill="#b0a58f", width=1)
    if not blank:
        if swap_name_position:
            draw.text((S(118), S(231)), "Senior Operations Analyst", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(448), S(231)), "Network Operations", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(118), S(291)), "Alexandra Hayes", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(398), S(291)), "Alex Hayes", font=FONT_VALUE_SMALL, fill="#2f2b23")
        else:
            draw.text((S(118), S(231)), "Alexandra Hayes", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(448), S(231)), "Alex Hayes", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(118), S(291)), "Senior Operations Analyst", font=FONT_VALUE_SMALL, fill="#2f2b23")
            draw.text((S(398), S(291)), "Network Operations", font=FONT_VALUE_SMALL, fill="#2f2b23")
        draw.text((S(118), S(359)), "2714 Red Cedar Lane", font=FONT_VALUE_SMALL, fill="#2f2b23")
        draw.text((S(118), S(377)), "Larkhaven, TX 78705", font=FONT_VALUE_SMALL, fill="#2f2b23")
        draw.text((S(368), S(352)), "Larkhaven, TX 78705", font=FONT_VALUE_SMALL, fill="#2f2b23")

        draw.text((S(110), S(428)), "(512) 555-0147", font=FONT_BODY, fill="#2f2b23")
        draw.text((S(255), S(428)), "(737) 555-0199", font=FONT_BODY, fill="#2f2b23")
        draw.text((S(430), S(428)), "(512) 555-0102", font=FONT_BODY, fill="#2f2b23")
        draw.text((S(110), S(470)), "alex.hayes@example.com", font=FONT_BODY, fill="#2f2b23")
        draw.text((S(345), S(470)), "M. Patel / (512) 555-0130", font=FONT_BODY, fill="#2f2b23")

    draw.rectangle((S(104), S(500), S(596), S(530)), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((S(116), S(507)), "Section 2. Recent Work History", font=FONT_SECTION, fill="#413828")

    # Reading-order challenge: labels first, values later in a separate row.
    history_rows = [
        {
            "y": 546,
            "employer": "Northwind Fulfillment",
            "address": "9101 Logistics Way, Brighthaven, TX",
            "dates": "03/2022 - 02/2026",
            "title": "Operations Coordinator",
            "supervisor": "J. Rivera",
            "reason": "Relocation of facility",
        },
        {
            "y": 660,
            "employer": "Capstone Field Services",
            "address": "4800 Mesa Park Dr, Stonecross, TX",
            "dates": "07/2019 - 02/2022",
            "title": "Customer Success Lead",
            "supervisor": "L. Chen",
            "reason": "Pursued internal operations role",
        },
    ]
    for row in history_rows[:num_history_rows]:
        y = S(row["y"])
        draw.text((S(110), y), "Employer name", font=FONT_BODY, fill="#6b6557")
        draw.text((S(280), y), "Employer address", font=FONT_BODY, fill="#6b6557")
        draw.text((S(500), y), "Dates employed", font=FONT_BODY, fill="#6b6557")
        draw.text((S(110), y + S(40)), "Job title", font=FONT_BODY, fill="#6b6557")
        draw.text((S(360), y + S(40)), "Supervisor name", font=FONT_BODY, fill="#6b6557")
        draw.text((S(110), y + S(72)), "Reason for leaving", font=FONT_BODY, fill="#6b6557")

        draw.line((S(110), y + S(26), S(250), y + S(26)), fill="#b0a58f", width=1)
        draw.line((S(280), y + S(26), S(470), y + S(26)), fill="#b0a58f", width=1)
        draw.line((S(500), y + S(26), S(586), y + S(26)), fill="#b0a58f", width=1)
        draw.line((S(110), y + S(66), S(330), y + S(66)), fill="#b0a58f", width=1)
        draw.line((S(360), y + S(66), S(586), y + S(66)), fill="#b0a58f", width=1)
        draw.line((S(110), y + S(96), S(586), y + S(96)), fill="#b0a58f", width=1)

        if not blank:
            draw.text((S(110), y + S(12)), row["employer"], font=FONT_BODY, fill="#2f2b23")
            draw.text((S(280), y + S(12)), row["address"], font=FONT_BODY, fill="#2f2b23")
            draw.text((S(500), y + S(12)), row["dates"], font=FONT_BODY, fill="#2f2b23")
            draw.text((S(110), y + S(52)), row["title"], font=FONT_BODY, fill="#2f2b23")
            draw.text((S(360), y + S(52)), row["supervisor"], font=FONT_BODY, fill="#2f2b23")
            draw.text((S(110), y + S(84)), row["reason"], font=FONT_BODY, fill="#2f2b23")

    # Shift Section 3+ up when the form has fewer history rows.
    s3_shift = 0 if num_history_rows >= 2 else 100

    draw.rectangle((S(104), S(760 - s3_shift), S(596), S(790 - s3_shift)), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((S(116), S(767 - s3_shift)), "Section 3. Availability and Certification", font=FONT_SECTION, fill="#413828")

    draw.text((S(110), S(800 - s3_shift)), "Earliest start date", font=FONT_BODY, fill="#6b6557")
    draw.text((S(335), S(800 - s3_shift)), "Available weekends?", font=FONT_BODY, fill="#6b6557")
    draw.text((S(486), S(800 - s3_shift)), "Badge renewal date", font=FONT_BODY, fill="#6b6557")
    draw.line((S(110), S(822 - s3_shift), S(260), S(822 - s3_shift)), fill="#b0a58f", width=1)
    draw.rectangle((S(335), S(818 - s3_shift), S(349), S(832 - s3_shift)), outline="#b0a58f", width=1)
    draw.rectangle((S(412), S(818 - s3_shift), S(426), S(832 - s3_shift)), outline="#b0a58f", width=1)
    draw.text((S(358), S(819 - s3_shift)), "Yes", font=FONT_TINY, fill="#6b6557")
    draw.text((S(435), S(819 - s3_shift)), "No", font=FONT_TINY, fill="#6b6557")
    draw.line((S(486), S(822 - s3_shift), S(586), S(822 - s3_shift)), fill="#b0a58f", width=1)

    if not blank:
        draw.text((S(110), S(808 - s3_shift)), "04/27/2026", font=FONT_BODY, fill="#2f2b23")
        draw.text((S(494), S(808 - s3_shift)), "05/15/2026", font=FONT_BODY, fill="#2f2b23")

    draw.text((S(110), S(844 - s3_shift)), "Disciplinary action within last 24 months?", font=FONT_BODY, fill="#6b6557")
    draw.rectangle((S(420), S(840 - s3_shift), S(434), S(854 - s3_shift)), outline="#b0a58f", width=1)
    draw.rectangle((S(486), S(840 - s3_shift), S(500), S(854 - s3_shift)), outline="#b0a58f", width=1)
    draw.text((S(444), S(841 - s3_shift)), "Yes", font=FONT_TINY, fill="#6b6557")
    draw.text((S(510), S(841 - s3_shift)), "No", font=FONT_TINY, fill="#6b6557")
    if not blank:
        draw.text((S(110), S(860 - s3_shift)), "Explain if yes on attached page.", font=FONT_TINY, fill="#6b6557")

    # Dense local context around the hard target with several distractor numbers nearby.
    dense_y = S(878 - s3_shift)
    draw.text((S(110), dense_y), "After a written offer, payroll records and I-9 support must be submitted within", font=FONT_MICRO, fill="#6b6557")
    prefix = "the shorter of 30 calendar days, 7 orientation days, or "
    draw.text((S(110), dense_y + S(16)), prefix, font=FONT_MICRO, fill="#6b6557")
    prefix_w = draw.textlength(prefix, font=FONT_MICRO)
    blank_x = S(110) + int(prefix_w)
    blank_w = S(24)
    blank_y = dense_y + S(16) + S(12)
    draw.line((blank_x, blank_y, blank_x + blank_w, blank_y), fill="#756a52", width=1)
    suffix_x = blank_x + blank_w + S(4)
    draw.text((suffix_x, dense_y + S(16)), "business days", font=FONT_MICRO, fill="#6b6557")
    draw.text((S(110), dense_y + S(30)), "after supervisor notice.", font=FONT_MICRO, fill="#6b6557")
    draw.text((S(110), dense_y + S(48)), "This deadline is separate from the 90-day review window and the 14-day badge reset.", font=FONT_MICRO, fill="#6b6557")
    if not blank:
        draw.text((blank_x + S(2), dense_y + S(12)), FIELDS[3].value, font=FONT_VALUE_SMALL, fill="#2f2b23")

    return image


def to_cv(image: Image.Image) -> np.ndarray:
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


def from_cv(image: np.ndarray) -> Image.Image:
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


def to_float_rgb(image: Image.Image) -> np.ndarray:
    return np.asarray(image).astype(np.float32) / 255.0


def from_float_rgb(array: np.ndarray) -> Image.Image:
    clipped = np.clip(array * 255.0, 0, 255).astype(np.uint8)
    return Image.fromarray(clipped, mode="RGB")


def smooth_noise(width: int, height: int, rng: np.random.Generator, scale: int) -> np.ndarray:
    small_w = max(2, width // scale)
    small_h = max(2, height // scale)
    base = rng.random((small_h, small_w), dtype=np.float32)
    return cv2.resize(base, (width, height), interpolation=cv2.INTER_CUBIC)


def generate_procedural_texture(kind: str, width: int, height: int, seed: int) -> Image.Image:
    rng = np.random.default_rng(seed)
    base = np.ones((height, width, 3), dtype=np.float32)
    if kind == "paper":
        tone = np.array([0.97, 0.95, 0.90], dtype=np.float32)
        base[:] = tone
        low = smooth_noise(width, height, rng, scale=12)[..., None]
        mid = smooth_noise(width, height, rng, scale=40)[..., None]
        base *= 0.96 + 0.08 * low
        base *= 0.98 + 0.04 * mid
    elif kind == "stain":
        base[:] = 1.0
        overlay = np.ones_like(base)
        stain_mask = smooth_noise(width, height, rng, scale=18)
        stain_mask = np.clip((stain_mask - 0.62) * 2.2, 0, 1)
        stain_color = np.array([0.74, 0.67, 0.52], dtype=np.float32)
        overlay[:] = stain_color
        base = base * (1 - stain_mask[..., None] * 0.35) + overlay * stain_mask[..., None] * 0.35
    elif kind == "desk":
        base[:] = np.array([0.76, 0.70, 0.62], dtype=np.float32)
        grain = smooth_noise(width, height, rng, scale=16)[..., None]
        base *= 0.88 + 0.24 * grain
    return from_float_rgb(base)


def load_texture_bank(kind: str, width: int, height: int) -> list[Image.Image]:
    texture_dir = TEXTURE_DIR / kind
    textures = []
    if texture_dir.exists():
        for path in sorted(texture_dir.glob("*.png")):
            textures.append(Image.open(path).convert("RGB").resize((width, height)))
    if not textures:
        for index in range(3):
            texture = generate_procedural_texture(kind, width, height, seed=101 + index * 17)
            output_path = OUTPUT_DIR / "textures" / f"{kind}-{index + 1}.png"
            texture.save(output_path)
            textures.append(texture)
    return textures


def blend_multiply(base: Image.Image, overlay: Image.Image, strength: float) -> Image.Image:
    a = to_float_rgb(base)
    b = to_float_rgb(overlay)
    mixed = a * ((1.0 - strength) + strength * b)
    return from_float_rgb(mixed)


def blend_overlay(base: Image.Image, overlay: Image.Image, strength: float) -> Image.Image:
    a = to_float_rgb(base)
    b = to_float_rgb(overlay)
    mixed = a * (1.0 - strength) + b * strength
    return from_float_rgb(mixed)


def apply_paper_texture(image: Image.Image, seed: int, stain_strength: float, paper_strength: float) -> Image.Image:
    paper = load_texture_bank("paper", *TEMPLATE_SIZE)[seed % 3]
    result = blend_multiply(image, paper, paper_strength)
    if stain_strength > 0:
        stain = load_texture_bank("stain", *TEMPLATE_SIZE)[(seed + 1) % 3]
        result = blend_overlay(result, stain, stain_strength)
    return result


def apply_ink_fade(image: Image.Image, fade_strength: float, seed: int) -> Image.Image:
    if fade_strength <= 0:
        return image
    rng = np.random.default_rng(seed)
    rgb = np.asarray(image).astype(np.float32)
    brightness = rgb.mean(axis=2)
    ink_mask = np.clip((220 - brightness) / 220, 0, 1)
    fade_map = 0.55 + 0.45 * smooth_noise(image.width, image.height, rng, scale=26)
    adjust = 1.0 - fade_strength * ink_mask * (1.0 - fade_map)
    faded = rgb * adjust[..., None] + 255 * (1 - adjust[..., None])
    return Image.fromarray(np.clip(faded, 0, 255).astype(np.uint8), mode="RGB")


def apply_morphological_noise(image: Image.Image, amount: float, seed: int) -> Image.Image:
    """Simulate ink bleed (dilation) and broken strokes (erosion) via morphological ops.

    Works on the full-color image — no binarization. Dark pixels are dilated to
    simulate ink spreading, then light salt-and-pepper specks are added.
    """
    if amount <= 0:
        return image
    img = to_cv(image)
    rng = np.random.default_rng(seed)

    # Dilate dark regions to simulate ink bleed
    k = 2 if amount < 0.5 else 3
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k))
    dilated = cv2.erode(img, kernel, iterations=1)  # erode in BGR = dilate dark ink
    alpha = min(amount * 0.6, 0.4)
    blended = cv2.addWeighted(img, 1.0 - alpha, dilated, alpha, 0)

    # Salt-and-pepper specks (printer dust)
    n_specks = int(amount * 800)
    h, w = blended.shape[:2]
    for _ in range(n_specks):
        x, y = rng.integers(0, w), rng.integers(0, h)
        shade = rng.integers(160, 230)
        blended[y, x] = [shade, shade, shade]

    return from_cv(blended)


def apply_print_streaks(image: Image.Image, strength: float, seed: int) -> Image.Image:
    """Vertical ink streaks from dirty printer rollers or toner cartridge."""
    if strength <= 0:
        return image
    rng = random.Random(seed)
    result = image.copy()
    draw = ImageDraw.Draw(result, "RGBA")
    w, h = image.size
    n_streaks = rng.randint(2, 5)
    for _ in range(n_streaks):
        x = rng.randint(int(w * 0.05), int(w * 0.95))
        thickness = rng.randint(1, 3)
        alpha = int(strength * rng.randint(25, 60))
        y0 = rng.randint(0, int(h * 0.1))
        y1 = rng.randint(int(h * 0.85), h)
        draw.rectangle((x, y0, x + thickness, y1), fill=(40, 35, 30, alpha))
    return result.convert("RGB")


def apply_toner_band(image: Image.Image, strength: float, seed: int) -> Image.Image:
    if strength <= 0:
        return image
    rng = np.random.default_rng(seed)
    rgb = to_float_rgb(image)
    band = smooth_noise(image.width, image.height, rng, scale=80)
    band = 1.0 - strength * 0.18 * band
    rgb *= band[..., None]
    return from_float_rgb(rgb)


def add_fold_shadows(image: Image.Image, strength: float, seed: int) -> Image.Image:
    if strength <= 0:
        return image
    rng = random.Random(seed)
    shaded = image.copy()
    draw = ImageDraw.Draw(shaded, "RGBA")
    img_w, img_h = image.size
    for _ in range(2):
        x = rng.randint(int(img_w * 0.1), int(img_w * 0.8))
        width = rng.randint(18, 34)
        alpha = int(45 * strength)
        draw.rectangle((x, int(img_h * 0.05), x + width, int(img_h * 0.95)), fill=(90, 80, 60, alpha))
        draw.rectangle((x + width, int(img_h * 0.05), x + width + 6, int(img_h * 0.95)), fill=(255, 255, 255, int(26 * strength)))
    return shaded.convert("RGB")
def jpeg_roundtrip(image: Image.Image, quality: int) -> Image.Image:
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality)
    buffer.seek(0)
    return Image.open(buffer).convert("RGB")


def add_random_lines(image: Image.Image, count: int, seed: int) -> Image.Image:
    rng = random.Random(seed)
    noisy = image.copy()
    draw = ImageDraw.Draw(noisy)
    for _ in range(count):
        x1 = rng.randint(80, 620)
        y1 = rng.randint(90, 790)
        x2 = x1 + rng.randint(-180, 180)
        y2 = y1 + rng.randint(-30, 30)
        color = rng.choice(["#58534a", "#6c6252", "#8e836a"])
        draw.line((x1, y1, x2, y2), fill=color, width=rng.randint(1, 2))
    return noisy


def add_random_dots(image: Image.Image, count: int, seed: int) -> Image.Image:
    rng = random.Random(seed)
    noisy = image.copy()
    draw = ImageDraw.Draw(noisy)
    for _ in range(count):
        x = rng.randint(70, 630)
        y = rng.randint(48, 828)
        r = 1 if rng.random() < 0.85 else 2
        shade = rng.randint(145, 220)
        draw.ellipse((x - r, y - r, x + r, y + r), fill=(shade, shade, shade))
    return noisy


def warp_perspective(image: Image.Image, offsets: list[tuple[int, int]]) -> Image.Image:
    x0, y0 = PAGE_BOX["x"], PAGE_BOX["y"]
    x1, y1 = x0 + PAGE_BOX["w"], y0 + PAGE_BOX["h"]
    src = np.float32([[x0, y0], [x1, y0], [x1, y1], [x0, y1]])
    dst = np.float32(
        [
            [x0 + S(offsets[0][0]), y0 + S(offsets[0][1])],
            [x1 + S(offsets[1][0]), y0 + S(offsets[1][1])],
            [x1 + S(offsets[2][0]), y1 + S(offsets[2][1])],
            [x0 + S(offsets[3][0]), y1 + S(offsets[3][1])],
        ]
    )
    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(
        to_cv(image),
        matrix,
        TEMPLATE_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(238, 227, 202),
    )
    return from_cv(warped)


def wave_displacement(image: Image.Image, amplitude: float, wavelength: float, seed: int) -> Image.Image:
    if amplitude <= 0:
        return image
    src = to_cv(image)
    h, w = src.shape[:2]
    xs, ys = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    phase = seed * 0.37
    offset_x = amplitude * np.sin(2 * np.pi * ys / wavelength + phase)
    offset_y = (amplitude * 0.55) * np.sin(2 * np.pi * xs / (wavelength * 1.4) + phase * 0.7)
    map_x = xs + offset_x.astype(np.float32)
    map_y = ys + offset_y.astype(np.float32)
    warped = cv2.remap(
        src,
        map_x,
        map_y,
        interpolation=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(238, 227, 202),
    )
    return from_cv(warped)


def rotate_scale(image: Image.Image, angle: float, scale_x: float, scale_y: float) -> Image.Image:
    w, h = TEMPLATE_SIZE
    src = np.float32([[0, 0], [w - 1, 0], [w - 1, h - 1], [0, h - 1]])
    center = np.array([w / 2.0, h / 2.0], dtype=np.float32)
    radians = math.radians(angle)
    rotation = np.array(
        [
            [math.cos(radians), -math.sin(radians)],
            [math.sin(radians), math.cos(radians)],
        ],
        dtype=np.float32,
    )
    scale = np.array([[scale_x, 0], [0, scale_y]], dtype=np.float32)
    transform = rotation @ scale
    dst = []
    for point in src:
        shifted = point - center
        mapped = transform @ shifted + center
        dst.append(mapped)
    matrix = cv2.getPerspectiveTransform(src, np.float32(dst))
    warped = cv2.warpPerspective(
        to_cv(image),
        matrix,
        TEMPLATE_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(238, 227, 202),
    )
    return from_cv(warped)


def shrink_and_offset(
    image: Image.Image,
    scale: float,
    offset_x: int,
    offset_y: int,
    background: tuple[int, int, int] = (236, 229, 210),
) -> Image.Image:
    if abs(scale - 1.0) < 1e-4 and offset_x == 0 and offset_y == 0:
        return image
    src = to_cv(image)
    h, w = src.shape[:2]
    matrix = np.float32(
        [
            [scale, 0.0, offset_x + (1.0 - scale) * w / 2.0],
            [0.0, scale, offset_y + (1.0 - scale) * h / 2.0],
        ]
    )
    warped = cv2.warpAffine(
        src,
        matrix,
        TEMPLATE_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=background,
    )
    return from_cv(warped)


PROFILES = [
    CorruptionProfile(
        id="clean",
        description="No corruption.",
        print_artifacts={"ink_fade": 0.0, "morph_noise": 0.0, "print_streaks": 0.0, "toner_band": 0.0},
        paper_artifacts={"paper_texture": 0.0, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="print",
        description="Printer artifacts only: ink bleed, vertical roller streaks, toner banding, and faded ink.",
        print_artifacts={"ink_fade": 0.10, "morph_noise": 0.12, "print_streaks": 0.10, "toner_band": 0.06},
        paper_artifacts={"paper_texture": 0.0, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="rotation",
        description="Mild skewed scan.",
        print_artifacts={"ink_fade": 0.03, "morph_noise": 0.0, "print_streaks": 0.0, "toner_band": 0.02},
        paper_artifacts={"paper_texture": 0.02, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 3.2, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="phone_photo",
        description="Phone photo from farther away with slight tilt, background, and mild capture blur.",
        print_artifacts={"ink_fade": 0.05, "morph_noise": 0.0, "print_streaks": 0.03, "toner_band": 0.03},
        paper_artifacts={"paper_texture": 0.05, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={
            "angle": 1.6,
            "scale_x": 1.0,
            "scale_y": 1.0,
            "perspective": [(-10, 12), (16, -8), (20, 18), (-12, -6)],
            "wave_amplitude": 0.0,
            "wave_length": 240.0,
            "frame_scale": 0.88,
            "offset_x": 18,
            "offset_y": 22,
        },
        capture={"blur": 0.55, "jpeg_quality": None, "lighting_gradient": 0.06, "camera_shadow": 0.08},
    ),
    CorruptionProfile(
        id="warp",
        description="Perspective warp with mild paper curl.",
        print_artifacts={"ink_fade": 0.03, "morph_noise": 0.0, "print_streaks": 0.02, "toner_band": 0.03},
        paper_artifacts={"paper_texture": 0.04, "stain_strength": 0.0, "fold_shadow": 0.08, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": [(-8, 10), (14, -6), (16, 12), (-14, -10)], "wave_amplitude": 1.4, "wave_length": 320.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.05, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="blur",
        description="Soft focus or scanner blur with slightly faded print.",
        print_artifacts={"ink_fade": 0.08, "morph_noise": 0.08, "print_streaks": 0.04, "toner_band": 0.04},
        paper_artifacts={"paper_texture": 0.03, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 1.1, "jpeg_quality": None, "lighting_gradient": 0.03, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="jpeg",
        description="Compressed upload with mild blur and low-ink print.",
        print_artifacts={"ink_fade": 0.11, "morph_noise": 0.10, "print_streaks": 0.08, "toner_band": 0.05},
        paper_artifacts={"paper_texture": 0.05, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.45, "jpeg_quality": 22, "lighting_gradient": 0.04, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="revised",
        description="Shorter form revision with only one employment history row. Section 3 shifts up, breaking template crop coordinates.",
        print_artifacts={"ink_fade": 0.0, "morph_noise": 0.0, "print_streaks": 0.0, "toner_band": 0.0},
        paper_artifacts={"paper_texture": 0.0, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="combo",
        description="Phone-photo style capture with low ink, stains, warp, blur, compression, and scribbles.",
        print_artifacts={"ink_fade": 0.16, "morph_noise": 0.15, "print_streaks": 0.12, "toner_band": 0.08},
        paper_artifacts={"paper_texture": 0.10, "stain_strength": 0.10, "fold_shadow": 0.30, "random_lines": 18, "random_dots": 180},
        geometry={"angle": 2.4, "scale_x": 1.03, "scale_y": 0.97, "perspective": [(-12, 16), (18, -8), (22, 20), (-18, -12)], "wave_amplitude": 2.8, "wave_length": 210.0},
        capture={"blur": 0.8, "jpeg_quality": 35, "lighting_gradient": 0.14, "camera_shadow": 0.12},
    ),
]


def apply_lighting_gradient(image: Image.Image, strength: float) -> Image.Image:
    if strength <= 0:
        return image
    rgb = to_float_rgb(image)
    h, w = rgb.shape[:2]
    x = np.linspace(0.0, 1.0, w, dtype=np.float32)
    y = np.linspace(0.0, 1.0, h, dtype=np.float32)
    xv, yv = np.meshgrid(x, y)
    gradient = 1.0 - strength * (0.55 * xv + 0.45 * yv)
    rgb *= gradient[..., None]
    return from_float_rgb(rgb)


def apply_camera_shadow(image: Image.Image, strength: float) -> Image.Image:
    if strength <= 0:
        return image
    rgb = to_float_rgb(image)
    h, w = rgb.shape[:2]
    x = np.linspace(-1.0, 1.0, w, dtype=np.float32)
    y = np.linspace(-1.0, 1.0, h, dtype=np.float32)
    xv, yv = np.meshgrid(x, y)
    vignette = np.exp(-(xv**2 + (yv * 1.2) ** 2) / 1.1)
    shadow = 1.0 - strength * (1.0 - vignette)
    rgb *= shadow[..., None]
    return from_float_rgb(rgb)


def apply_motion_blur(image: Image.Image, radius: float, angle_deg: float) -> Image.Image:
    if radius <= 0:
        return image
    size = max(3, int(round(radius * 6)))
    if size % 2 == 0:
        size += 1
    kernel = np.zeros((size, size), dtype=np.float32)
    kernel[size // 2, :] = 1.0
    center = (size / 2 - 0.5, size / 2 - 0.5)
    rotation = cv2.getRotationMatrix2D(center, angle_deg, 1.0)
    kernel = cv2.warpAffine(kernel, rotation, (size, size))
    kernel_sum = kernel.sum()
    if kernel_sum > 0:
        kernel /= kernel_sum
    blurred = cv2.filter2D(to_cv(image), -1, kernel)
    return from_cv(blurred)


def apply_focus_falloff(image: Image.Image, radius: float, seed: int) -> Image.Image:
    if radius <= 0:
        return image
    rng = random.Random(seed)
    sharp = to_float_rgb(image)
    heavy = to_float_rgb(image.filter(ImageFilter.GaussianBlur(radius=radius)))
    h, w = sharp.shape[:2]
    x = np.linspace(0.0, 1.0, w, dtype=np.float32)
    y = np.linspace(0.0, 1.0, h, dtype=np.float32)
    xv, yv = np.meshgrid(x, y)
    cx = 0.46 + rng.uniform(-0.06, 0.08)
    cy = 0.42 + rng.uniform(-0.05, 0.07)
    sx = 0.22 + rng.uniform(-0.03, 0.04)
    sy = 0.26 + rng.uniform(-0.04, 0.05)
    sharp_mask = np.exp(-(((xv - cx) ** 2) / (2 * sx * sx) + ((yv - cy) ** 2) / (2 * sy * sy)))
    sharp_mask = np.clip(0.25 + 0.85 * sharp_mask, 0.0, 1.0)[..., None]
    mixed = sharp * sharp_mask + heavy * (1.0 - sharp_mask)
    return from_float_rgb(mixed)


def apply_capture_pipeline(image: Image.Image, capture: dict[str, Any], seed: int) -> Image.Image:
    result = image
    result = apply_lighting_gradient(result, capture.get("lighting_gradient", 0.0))
    result = apply_camera_shadow(result, capture.get("camera_shadow", 0.0))
    blur = capture.get("blur", 0.0)
    if blur:
        result = apply_motion_blur(result, radius=max(0.6, blur * 0.9), angle_deg=8 + (seed % 9) * 7)
        result = apply_focus_falloff(result, radius=blur * 1.35, seed=seed + 19)
    jpeg_quality = capture.get("jpeg_quality")
    if jpeg_quality:
        result = jpeg_roundtrip(result, quality=jpeg_quality)
    return result


def apply_geometry_pipeline(image: Image.Image, geometry: dict[str, Any], seed: int) -> Image.Image:
    result = image
    perspective = geometry.get("perspective")
    if perspective:
        result = warp_perspective(result, perspective)
    angle = geometry.get("angle", 0.0)
    scale_x = geometry.get("scale_x", 1.0)
    scale_y = geometry.get("scale_y", 1.0)
    if angle or scale_x != 1.0 or scale_y != 1.0:
        result = rotate_scale(result, angle=angle, scale_x=scale_x, scale_y=scale_y)
    wave_amp = geometry.get("wave_amplitude", 0.0)
    if wave_amp:
        result = wave_displacement(result, amplitude=wave_amp, wavelength=geometry.get("wave_length", 240.0), seed=seed)
    frame_scale = geometry.get("frame_scale", 1.0)
    offset_x = geometry.get("offset_x", 0)
    offset_y = geometry.get("offset_y", 0)
    if frame_scale != 1.0 or offset_x or offset_y:
        result = shrink_and_offset(result, scale=frame_scale, offset_x=offset_x, offset_y=offset_y)
    return result


def apply_print_pipeline(image: Image.Image, print_artifacts: dict[str, Any], seed: int) -> Image.Image:
    result = image
    result = apply_ink_fade(result, print_artifacts.get("ink_fade", 0.0), seed)
    result = apply_morphological_noise(result, print_artifacts.get("morph_noise", 0.0), seed + 5)
    result = apply_print_streaks(result, print_artifacts.get("print_streaks", 0.0), seed + 7)
    result = apply_toner_band(result, print_artifacts.get("toner_band", 0.0), seed + 9)
    return result


def apply_paper_pipeline(image: Image.Image, paper_artifacts: dict[str, Any], seed: int) -> Image.Image:
    result = image
    result = apply_paper_texture(
        result,
        seed=seed,
        stain_strength=paper_artifacts.get("stain_strength", 0.0),
        paper_strength=paper_artifacts.get("paper_texture", 0.0),
    )
    result = add_fold_shadows(result, paper_artifacts.get("fold_shadow", 0.0), seed)
    lines = paper_artifacts.get("random_lines", 0)
    if lines:
        result = add_random_lines(result, count=lines, seed=seed + 31)
    dots = paper_artifacts.get("random_dots", 0)
    if dots:
        result = add_random_dots(result, count=dots, seed=seed + 47)
    return result


def apply_profile(profile: CorruptionProfile, image: Image.Image, seed: int) -> Image.Image:
    result = image.copy()
    result = apply_print_pipeline(result, profile.print_artifacts, seed)
    result = apply_paper_pipeline(result, profile.paper_artifacts, seed)
    result = apply_geometry_pipeline(result, profile.geometry, seed)
    result = apply_capture_pipeline(result, profile.capture, seed)
    return result


def build_match_visualization(
    template: np.ndarray,
    target: np.ndarray,
    kp1,
    kp2,
    matches,
    inlier_mask: np.ndarray | None,
    output_path: Path,
) -> None:
    if not matches:
        side_by_side = np.hstack([template, target])
        cv2.imwrite(str(output_path), side_by_side)
        return

    if inlier_mask is not None:
        filtered = [match for match, keep in zip(matches, inlier_mask.ravel().tolist(), strict=False) if keep]
    else:
        filtered = list(matches)
    chosen = filtered if filtered else list(matches)
    chosen = sorted(chosen, key=lambda match: match.distance)

    if len(chosen) > 28:
        step = max(1, len(chosen) // 28)
        chosen = chosen[::step][:28]

    visualization = cv2.drawMatches(
        template,
        kp1,
        target,
        kp2,
        chosen,
        None,
        matchColor=(64, 196, 120),
        singlePointColor=(215, 186, 120),
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
    )
    cv2.imwrite(str(output_path), visualization)


def match_and_register(template: np.ndarray, target: np.ndarray, match_output_path: Path) -> tuple[np.ndarray | None, dict]:
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=5000, fastThreshold=5)
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(target_gray, None)
    if des1 is None or des2 is None:
        build_match_visualization(template, target, kp1 or [], kp2 or [], [], None, match_output_path)
        return None, {"ok": False, "reason": "no_descriptors"}
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    knn = matcher.knnMatch(des1, des2, k=2)
    good = []
    for pair in knn:
        if len(pair) != 2:
            continue
        m, n = pair
        if m.distance < 0.75 * n.distance:
            good.append(m)
    if len(good) < 12:
        build_match_visualization(template, target, kp1, kp2, good, None, match_output_path)
        return None, {"ok": False, "reason": "too_few_matches", "matches": len(good)}

    src = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if homography is None:
        build_match_visualization(template, target, kp1, kp2, good, None, match_output_path)
        return None, {"ok": False, "reason": "homography_failed", "matches": len(good)}
    build_match_visualization(template, target, kp1, kp2, good, mask, match_output_path)
    registered = cv2.warpPerspective(
        target,
        homography,
        TEMPLATE_SIZE,
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(238, 227, 202),
    )
    inliers = int(mask.sum()) if mask is not None else 0
    return registered, {
        "ok": True,
        "matches": len(good),
        "inliers": inliers,
        "inlier_ratio": round(inliers / max(len(good), 1), 4),
    }


def crop_with_padding(image: np.ndarray, field: Field) -> np.ndarray:
    x, y, w, h = field.box
    pad_map = {
        "name": (6, 8, 6, 8),
        "position": (6, 8, 6, 8),
        "address": (0, 12, 12, 12),
        "records_days": (2, 6, 8, 2),
    }
    left, top, right, bottom = pad_map.get(field.id, (8, 8, 8, 8))
    x0 = max(0, x - left)
    y0 = max(0, y - top)
    x1 = min(image.shape[1], x + w + right)
    y1 = min(image.shape[0], y + h + bottom)
    return image[y0:y1, x0:x1]


def preprocess_for_ocr(crop: np.ndarray, field: Field) -> np.ndarray:
    """Minimal preprocessing: white border only. Doctr handles its own resizing."""
    bordered = cv2.copyMakeBorder(
        crop, 10, 10, 10, 10, borderType=cv2.BORDER_CONSTANT, value=(255, 255, 255)
    )
    return bordered


def save_crop(image: np.ndarray, field: Field, variant_name: str) -> tuple[Path, Path]:
    """Save raw crop for display and preprocessed crop for OCR. Returns (display_path, ocr_path)."""
    crop = crop_with_padding(image, field)
    display_path = OUTPUT_DIR / "crops" / f"{variant_name}-{field.id}.png"
    cv2.imwrite(str(display_path), crop)
    ocr_crop = preprocess_for_ocr(crop, field)
    ocr_path = OUTPUT_DIR / "crops" / f"{variant_name}-{field.id}-ocr.png"
    cv2.imwrite(str(ocr_path), ocr_crop)
    return display_path, ocr_path


def normalize_text(value: str) -> str:
    """Strip non-alphanumeric chars and lowercase for comparison."""
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def texts_match(expected: str, ocr_text: str) -> bool:
    """Check if OCR output matches expected value. Uses exact match after normalization."""
    return normalize_text(expected) == normalize_text(ocr_text)


def doctr_ocr_predictor():
    from doctr.models import ocr_predictor

    return ocr_predictor(pretrained=True)


def doctr_extract_text(predictor, image_paths: list[Path]) -> list[str]:
    from doctr.io import DocumentFile

    results = []
    for path in image_paths:
        doc = DocumentFile.from_images(str(path))
        result = predictor(doc)
        rendered = result.render()
        text = " ".join(rendered.split()) if rendered else ""
        # Fallback to tesseract when doctr returns empty (happens with isolated short text)
        if not text.strip():
            text = tesseract_extract_text(path)
        results.append(text)
    return results


def tesseract_extract_text(image_path: Path) -> str:
    import pytesseract

    img = cv2.imread(str(image_path))
    text = pytesseract.image_to_string(img, config="--psm 7")  # single line mode
    return " ".join(text.split())


def generate_manifest() -> dict:
    ensure_dirs()
    clear_generated_outputs()
    blank = render_template(blank=True)
    filled = render_template(blank=False)

    blank_path = OUTPUT_DIR / "template-blank.png"
    filled_path = OUTPUT_DIR / "template-filled.png"
    blank.save(blank_path)
    filled.save(filled_path)

    predictor = doctr_ocr_predictor()
    template_cv = to_cv(blank)
    filled_cv = to_cv(filled)

    variants = []

    revised_filled = render_template(blank=False, num_history_rows=1, swap_name_position=True)

    for index, profile in enumerate(PROFILES):
        base_image = revised_filled if profile.id == "revised" else filled
        variant_image = apply_profile(profile, base_image, seed=400 + index * 13)
        variant_path = OUTPUT_DIR / "variants" / f"{profile.id}.png"
        variant_image.save(variant_path)
        match_path = OUTPUT_DIR / "matching" / f"{profile.id}-matches.png"

        registered_cv, match_info = match_and_register(template_cv, to_cv(variant_image), match_path)
        crop_paths = []
        field_results = []

        if registered_cv is not None:
            registered_path = OUTPUT_DIR / "variants" / f"{profile.id}-registered.png"
            cv2.imwrite(str(registered_path), registered_cv)
            display_paths = []
            ocr_paths = []
            for field in FIELDS:
                display_path, ocr_path = save_crop(registered_cv, field, profile.id)
                display_paths.append(display_path)
                ocr_paths.append(ocr_path)
            ocr_texts = doctr_extract_text(predictor, ocr_paths)
            for field, ocr_text, display_path in zip(FIELDS, ocr_texts, display_paths):
                correct = texts_match(field.value, ocr_text)
                field_results.append(
                    {
                        "id": field.id,
                        "label": field.label,
                        "expected": field.value,
                        "ocr_text": ocr_text,
                        "correct": bool(correct),
                        "crop": str(display_path.relative_to(OUTPUT_DIR)),
                    }
                )
        else:
            for field in FIELDS:
                field_results.append(
                    {
                        "id": field.id,
                        "label": field.label,
                        "expected": field.value,
                        "ocr_text": "",
                        "correct": False,
                        "crop": "",
                    }
                )

        variants.append(
            {
                "id": profile.id,
                "description": profile.description,
                "image": str(variant_path.relative_to(OUTPUT_DIR)),
                "matching_visualization": str(match_path.relative_to(OUTPUT_DIR)),
                "profile": {
                    "print_artifacts": profile.print_artifacts,
                    "paper_artifacts": profile.paper_artifacts,
                    "geometry": profile.geometry,
                    "capture": profile.capture,
                },
                "registration": match_info,
                "all_fields_correct": all(item["correct"] for item in field_results),
                "fields": field_results,
            }
        )

    manifest = {
        "template": {
            "blank_image": str(blank_path.relative_to(OUTPUT_DIR)),
            "filled_image": str(filled_path.relative_to(OUTPUT_DIR)),
            "size": {"width": TEMPLATE_SIZE[0], "height": TEMPLATE_SIZE[1]},
            "page": PAGE_BOX,
            "fields": [
                {"id": field.id, "label": field.label, "value": field.value, "box": field.box}
                for field in FIELDS
            ],
        },
        "variants": variants,
    }
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=7)
    parser.parse_args()

    random.seed(7)
    np.random.seed(7)

    manifest = generate_manifest()
    output_path = OUTPUT_DIR / "room1-manifest.json"
    output_path.write_text(json.dumps(manifest, indent=2))
    print(f"Wrote {output_path}")
    for variant in manifest["variants"]:
        reg = variant["registration"]
        print(
            f"{variant['id']:>8}  match_ok={reg.get('ok')}  "
            f"fields_ok={variant['all_fields_correct']}  "
            f"matches={reg.get('matches', 0)}  inliers={reg.get('inliers', 0)}"
        )


if __name__ == "__main__":
    main()
