#!/usr/bin/env python3
"""Generate PWA icons for Cosmic Crystal."""
from PIL import Image, ImageDraw, ImageFilter
import math

def create_icon(size):
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Background circle
    margin = int(size * 0.04)
    draw.ellipse([margin, margin, size - margin, size - margin],
                 fill=(6, 6, 20, 255))

    # Outer glow ring
    ring_margin = int(size * 0.06)
    draw.ellipse([ring_margin, ring_margin, size - ring_margin, size - ring_margin],
                 outline=(102, 204, 255, 80), width=max(1, size // 64))

    # Crystal polygon points (scaled)
    cx, cy = size / 2, size / 2
    s = size * 0.38

    def pt(px, py):
        return (cx + px * s / 100, cy + py * s / 100)

    crystal_pts = [
        pt(0, -100), pt(45, -45), pt(55, 5),
        pt(30, 60), pt(0, 85), pt(-30, 60),
        pt(-55, 5), pt(-45, -45)
    ]

    # Shadow/glow layer
    glow_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_img)
    glow_draw.polygon(crystal_pts, fill=(102, 204, 255, 60))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=size * 0.06))
    img = Image.alpha_composite(img, glow_img)
    draw = ImageDraw.Draw(img)

    # Main crystal body - gradient simulation with multiple polygons
    # Base color (pink-purple)
    draw.polygon(crystal_pts, fill=(192, 132, 252, 230))

    # Upper half lighter (cyan tint)
    upper_pts = [
        pt(0, -100), pt(45, -45), pt(55, 5),
        pt(0, 30), pt(-55, 5), pt(-45, -45)
    ]
    draw.polygon(upper_pts, fill=(102, 204, 255, 140))

    # Top highlight
    top_pts = [pt(0, -100), pt(20, -50), pt(0, -10), pt(-20, -50)]
    draw.polygon(top_pts, fill=(255, 255, 255, 80))

    # Inner shine
    shine_pts = [pt(0, -100), pt(15, -55), pt(0, -20), pt(-15, -55)]
    draw.polygon(shine_pts, fill=(255, 255, 255, 50))

    # Outline
    draw.polygon(crystal_pts, outline=(200, 220, 255, 120), width=max(1, size // 96))

    # Stars around crystal
    star_positions = [
        (0.15, 0.15), (0.85, 0.15), (0.15, 0.85), (0.85, 0.85),
        (0.5, 0.08), (0.08, 0.5), (0.92, 0.5), (0.5, 0.92)
    ]
    for sx, sy in star_positions:
        star_x, star_y = int(sx * size), int(sy * size)
        r = max(1, size // 48)
        draw.ellipse([star_x - r, star_y - r, star_x + r, star_y + r],
                     fill=(255, 255, 255, 120))

    return img

for sz in [192, 512]:
    icon = create_icon(sz)
    icon.save(f'icons/icon-{sz}.png', 'PNG')
    print(f'Created icons/icon-{sz}.png')

print('Done!')
