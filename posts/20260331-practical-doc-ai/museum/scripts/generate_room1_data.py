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
TEMPLATE_SIZE = (700, 900)
PAGE_BOX = {"x": 70, "y": 48, "w": 560, "h": 780}


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
    Field("name", "Applicant name", "Alexandra Hayes", (106, 224, 320, 30)),
    Field("position", "Position desired", "Senior Operations Analyst", (106, 285, 380, 30)),
    Field("address", "Street address", "2714 Red Cedar Lane, Austin, TX", (106, 346, 430, 56)),
    Field("records_days", "Records due (days)", "3", (142, 741, 82, 18)),
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


FONT_TITLE = load_font("Georgia.ttf", 24)
FONT_SUBTITLE = load_font("Georgia.ttf", 14)
FONT_LABEL = load_font("Georgia.ttf", 14)
FONT_VALUE = load_font("Georgia.ttf", 16)
FONT_VALUE_SMALL = load_font("Georgia.ttf", 14)
FONT_BODY = load_font("Georgia.ttf", 13)
FONT_SECTION = load_font("Georgia.ttf", 14)
FONT_TINY = load_font("Georgia.ttf", 12)
FONT_MICRO = load_font("Georgia.ttf", 11)


def ensure_dirs() -> None:
    (OUTPUT_DIR / "variants").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "crops").mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "textures").mkdir(parents=True, exist_ok=True)


def clear_generated_outputs() -> None:
    for pattern in ["variants/*.png", "crops/*.png", "template-blank.png", "template-filled.png", "room1-manifest.json"]:
        for path in OUTPUT_DIR.glob(pattern):
            if path.is_file():
                path.unlink()


def render_template(blank: bool = True) -> Image.Image:
    image = Image.new("RGB", TEMPLATE_SIZE, "#eee3ca")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, 699, 899), fill="#eee3ca")
    px, py, pw, ph = PAGE_BOX["x"], PAGE_BOX["y"], PAGE_BOX["w"], PAGE_BOX["h"]
    draw.rectangle((px, py, px + pw, py + ph), fill="#f9f6eb", outline="#9d9278", width=2)

    draw.ellipse((94, 72, 146, 124), fill="#d7ccb4", outline="#8e836a", width=2)
    draw.text((164, 74), "Employment Application", font=FONT_TITLE, fill="#332b1d")
    draw.text((164, 101), "Northwind Logistics", font=FONT_SUBTITLE, fill="#5a533f")
    draw.text(
        (164, 121),
        "Applicant intake form for hourly and salaried roles",
        font=FONT_BODY,
        fill="#5a533f",
    )

    draw.rectangle((104, 164, 596, 194), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((116, 171), "Section 1. Applicant Information", font=FONT_SECTION, fill="#413828")

    labels = [
        ("Applicant name", (106, 206)),
        ("Position desired", (106, 267)),
        ("Street address", (106, 328)),
    ]
    for text, xy in labels:
        draw.text(xy, text, font=FONT_LABEL, fill="#574f40")

    for field in FIELDS:
        x, y, w, h = field.box
        if field.id == "records_days":
            draw.line((x + 8, y + h - 4, x + 26, y + h - 4), fill="#756a52", width=1)
        else:
            draw.rectangle((x, y, x + w, y + h), outline="#756a52", width=1)

    if not blank:
        draw.text((118, 228), FIELDS[0].value, font=FONT_VALUE, fill="#2f2b23")
        draw.text((118, 289), FIELDS[1].value, font=FONT_VALUE, fill="#2f2b23")
        draw.text((118, 350), "2714 Red Cedar Lane", font=FONT_VALUE_SMALL, fill="#2f2b23")
        draw.text((118, 369), "Austin, TX", font=FONT_VALUE_SMALL, fill="#2f2b23")

    draw.rectangle((104, 420, 596, 450), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((116, 427), "Section 2. Work History", font=FONT_SECTION, fill="#413828")

    body_lines = [
        ("Employer name", (106, 484), (106, 490, 322, 490)),
        ("Dates employed", (362, 484), (362, 490, 540, 490)),
        ("Job title", (106, 512), (106, 518, 540, 518)),
        ("Employer name", (106, 568), (106, 574, 322, 574)),
        ("Dates employed", (362, 568), (362, 574, 540, 574)),
        ("Job title", (106, 596), (106, 602, 540, 602)),
    ]
    for text, label_xy, line in body_lines:
        draw.text(label_xy, text, font=FONT_BODY, fill="#6b6557")
        draw.line(line, fill="#b0a58f", width=1)

    draw.rectangle((104, 644, 596, 674), fill="#e5ddca", outline="#9d9278", width=1)
    draw.text((116, 651), "Section 3. Availability and Certification", font=FONT_SECTION, fill="#413828")
    draw.text((106, 706), "Earliest start date", font=FONT_BODY, fill="#6b6557")
    draw.text((328, 706), "Available weekends?", font=FONT_BODY, fill="#6b6557")
    draw.line((106, 712, 260, 712), fill="#b0a58f", width=1)
    draw.rectangle((328, 691, 342, 705), outline="#b0a58f", width=1)
    draw.rectangle((410, 691, 424, 705), outline="#b0a58f", width=1)
    draw.text((348, 693), "Yes", font=FONT_TINY, fill="#6b6557")
    draw.text((430, 693), "No", font=FONT_TINY, fill="#6b6557")

    dense_y = 724
    dense_line_1 = "After a written offer, missing employment records must be submitted"
    dense_prefix = "within"
    dense_suffix = "business days or the applicant start date may be delayed."
    dense_line_3 = "The hiring team should also be notified of scheduling conflicts before the first shift."
    draw.text((106, dense_y), dense_line_1, font=FONT_MICRO, fill="#6b6557")
    prefix_bbox = draw.textbbox((106, dense_y + 15), dense_prefix, font=FONT_MICRO)
    draw.text((106, dense_y + 15), dense_prefix, font=FONT_MICRO, fill="#6b6557")
    blank_x = prefix_bbox[2] + 10
    blank_y = dense_y + 25
    blank_w = 18
    draw.line((blank_x, blank_y, blank_x + blank_w, blank_y), fill="#756a52", width=1)
    draw.text((blank_x + blank_w + 8, dense_y + 15), dense_suffix, font=FONT_MICRO, fill="#6b6557")
    draw.text((106, dense_y + 30), dense_line_3, font=FONT_MICRO, fill="#6b6557")
    if not blank:
        draw.text((blank_x + 4, dense_y + 10), FIELDS[3].value, font=FONT_TINY, fill="#2f2b23")

    draw.text(
        (106, 778),
        "I certify the information above is complete and accurate to the best of my knowledge.",
        font=FONT_BODY,
        fill="#6b6557",
    )
    draw.line((106, 808, 350, 808), fill="#b0a58f", width=1)
    draw.line((390, 808, 540, 808), fill="#b0a58f", width=1)
    draw.text((106, 816), "Applicant signature", font=FONT_TINY, fill="#6b6557")
    draw.text((390, 816), "Date", font=FONT_TINY, fill="#6b6557")

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


def apply_stroke_breakage(image: Image.Image, amount: float) -> Image.Image:
    if amount <= 0:
        return image
    gray = cv2.cvtColor(to_cv(image), cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 185, 255, cv2.THRESH_BINARY_INV)
    iterations = 1 if amount < 0.45 else 2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    eroded = cv2.erode(binary, kernel, iterations=iterations)
    restored = 255 - eroded
    color = cv2.cvtColor(restored, cv2.COLOR_GRAY2BGR)
    base = cv2.addWeighted(to_cv(image), 0.55, color, 0.45, 0)
    return from_cv(base)


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
    for _ in range(2):
        x = rng.randint(140, 560)
        width = rng.randint(18, 34)
        alpha = int(45 * strength)
        draw.rectangle((x, 90, x + width, 810), fill=(90, 80, 60, alpha))
        draw.rectangle((x + width, 90, x + width + 6, 810), fill=(255, 255, 255, int(26 * strength)))
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
    src = np.float32([[70, 48], [630, 48], [630, 828], [70, 828]])
    dst = np.float32(
        [
            [70 + offsets[0][0], 48 + offsets[0][1]],
            [630 + offsets[1][0], 48 + offsets[1][1]],
            [630 + offsets[2][0], 828 + offsets[2][1]],
            [70 + offsets[3][0], 828 + offsets[3][1]],
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
    src = np.float32([[0, 0], [699, 0], [699, 899], [0, 899]])
    center = np.array([350.0, 450.0], dtype=np.float32)
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
        print_artifacts={"ink_fade": 0.0, "stroke_breakage": 0.0, "toner_band": 0.0},
        paper_artifacts={"paper_texture": 0.0, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="rotation",
        description="Mild skewed scan.",
        print_artifacts={"ink_fade": 0.03, "stroke_breakage": 0.0, "toner_band": 0.02},
        paper_artifacts={"paper_texture": 0.02, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 3.2, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.0, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="phone_photo",
        description="Phone photo from farther away with slight tilt, background, and mild capture blur.",
        print_artifacts={"ink_fade": 0.05, "stroke_breakage": 0.03, "toner_band": 0.03},
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
        print_artifacts={"ink_fade": 0.03, "stroke_breakage": 0.02, "toner_band": 0.03},
        paper_artifacts={"paper_texture": 0.04, "stain_strength": 0.0, "fold_shadow": 0.08, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": [(-8, 10), (14, -6), (16, 12), (-14, -10)], "wave_amplitude": 1.4, "wave_length": 320.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.05, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="blur",
        description="Soft focus or scanner blur with slightly faded print.",
        print_artifacts={"ink_fade": 0.08, "stroke_breakage": 0.04, "toner_band": 0.04},
        paper_artifacts={"paper_texture": 0.03, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 1.1, "jpeg_quality": None, "lighting_gradient": 0.03, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="jpeg",
        description="Compressed upload with mild blur and low-ink print.",
        print_artifacts={"ink_fade": 0.11, "stroke_breakage": 0.08, "toner_band": 0.05},
        paper_artifacts={"paper_texture": 0.05, "stain_strength": 0.0, "fold_shadow": 0.0, "random_lines": 0, "random_dots": 0},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.45, "jpeg_quality": 22, "lighting_gradient": 0.04, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="lines",
        description="Marked-up and dusty paper with pen lines, fold shadows, and scan specks.",
        print_artifacts={"ink_fade": 0.05, "stroke_breakage": 0.03, "toner_band": 0.03},
        paper_artifacts={"paper_texture": 0.05, "stain_strength": 0.02, "fold_shadow": 0.22, "random_lines": 22, "random_dots": 180},
        geometry={"angle": 0.0, "scale_x": 1.0, "scale_y": 1.0, "perspective": None, "wave_amplitude": 0.0, "wave_length": 240.0},
        capture={"blur": 0.0, "jpeg_quality": None, "lighting_gradient": 0.02, "camera_shadow": 0.0},
    ),
    CorruptionProfile(
        id="combo",
        description="Phone-photo style capture with low ink, stains, warp, blur, compression, and scribbles.",
        print_artifacts={"ink_fade": 0.16, "stroke_breakage": 0.12, "toner_band": 0.08},
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
    result = apply_stroke_breakage(result, print_artifacts.get("stroke_breakage", 0.0))
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


def match_and_register(template: np.ndarray, target: np.ndarray) -> tuple[np.ndarray | None, dict]:
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    orb = cv2.ORB_create(nfeatures=5000, fastThreshold=5)
    kp1, des1 = orb.detectAndCompute(template_gray, None)
    kp2, des2 = orb.detectAndCompute(target_gray, None)
    if des1 is None or des2 is None:
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
        return None, {"ok": False, "reason": "too_few_matches", "matches": len(good)}

    src = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    dst = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    homography, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
    if homography is None:
        return None, {"ok": False, "reason": "homography_failed", "matches": len(good)}
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
        "records_days": (16, 8, 68, 12),
    }
    left, top, right, bottom = pad_map.get(field.id, (8, 8, 8, 8))
    x0 = max(0, x - left)
    y0 = max(0, y - top)
    x1 = min(image.shape[1], x + w + right)
    y1 = min(image.shape[0], y + h + bottom)
    return image[y0:y1, x0:x1]


def preprocess_for_ocr(crop: np.ndarray, field: Field) -> np.ndarray:
    scale_map = {
        "name": 3.0,
        "position": 3.0,
        "address": 3.5,
        "records_days": 5.5,
    }
    scale = scale_map.get(field.id, 3.0)
    enlarged = cv2.resize(crop, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
    gray = cv2.cvtColor(enlarged, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    gray = cv2.normalize(gray, None, 0, 255, cv2.NORM_MINMAX)
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        11,
    )
    bordered = cv2.copyMakeBorder(
        thresh,
        24,
        24,
        24,
        24,
        borderType=cv2.BORDER_CONSTANT,
        value=255,
    )
    return cv2.cvtColor(bordered, cv2.COLOR_GRAY2BGR)


def save_crop(image: np.ndarray, field: Field, variant_name: str) -> Path:
    crop = crop_with_padding(image, field)
    crop = preprocess_for_ocr(crop, field)
    path = OUTPUT_DIR / "crops" / f"{variant_name}-{field.id}.png"
    cv2.imwrite(str(path), crop)
    return path


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", value.lower())


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
        results.append(text)
    return results


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

    for index, profile in enumerate(PROFILES):
        variant_image = apply_profile(profile, filled, seed=400 + index * 13)
        variant_path = OUTPUT_DIR / "variants" / f"{profile.id}.png"
        variant_image.save(variant_path)

        registered_cv, match_info = match_and_register(template_cv, to_cv(variant_image))
        crop_paths = []
        field_results = []

        if registered_cv is not None:
            registered_path = OUTPUT_DIR / "variants" / f"{profile.id}-registered.png"
            cv2.imwrite(str(registered_path), registered_cv)
            for field in FIELDS:
                crop_paths.append(save_crop(registered_cv, field, profile.id))
            ocr_texts = doctr_extract_text(predictor, crop_paths)
            for field, ocr_text, crop_path in zip(FIELDS, ocr_texts, crop_paths):
                correct = normalize_text(field.value) in normalize_text(ocr_text)
                field_results.append(
                    {
                        "id": field.id,
                        "label": field.label,
                        "expected": field.value,
                        "ocr_text": ocr_text,
                        "correct": bool(correct),
                        "crop": str(crop_path.relative_to(ASSET_DIR)),
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
                "image": str(variant_path.relative_to(ASSET_DIR)),
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
            "blank_image": str(blank_path.relative_to(ASSET_DIR)),
            "filled_image": str(filled_path.relative_to(ASSET_DIR)),
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
