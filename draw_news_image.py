#!/usr/bin/env python3
"""Draw the 21 November 2026 world-news front page (1024x1024 PNG).

One image, five verified stories, drawn with Pillow only. Every fact on
the page was checked against reports published on 20 November 2026
(see README.md for the sources). The page is drawn early on 21 November
UTC, so the Friday 20 November stories are dated as such on the page.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 243, 230)
INK = (16, 16, 16)
RED = (176, 32, 32)
BLUE = (22, 64, 122)
GREY = (92, 88, 78)
RULE = (16, 16, 16)
GOLD = (198, 158, 28)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap; returns lines fitting `width` px."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, leading, color=INK):
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def kicker(draw, x, y, text):
    f = font(SANS_B, 18)
    draw.text((x, y), text, font=f, fill=RED)
    return y + 25


def box(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], outline=RULE, width=2)


def bridges(draw, x, y, w, h):
    """Three bridge arcs over a river, with missile streaks above."""
    # Sky streaks: three descending missile trails.
    for sx, sy, ln in [(x + 20, y + 8, 70), (x + 110, y + 2, 84),
                       (x + 200, y + 12, 64)]:
        draw.line([sx, sy, sx + ln, sy + 26], fill=RED, width=4)
        draw.ellipse([sx + ln - 4, sy + 22, sx + ln + 4, sy + 30],
                     fill=RED)
    # River.
    draw.rectangle([x, y + h - 26, x + w, y + h], fill=BLUE)
    # Three arched bridges.
    for i, bx in enumerate([x + 8, x + w // 3 + 2, x + 2 * w // 3 - 4]):
        bw = w // 3 - 12
        draw.arc([bx, y + h - 78, bx + bw, y + h - 8],
                 start=180, end=360, fill=INK, width=5)
        draw.line([bx, y + h - 44, bx + bw, y + h - 44], fill=INK, width=3)
        if i == 1:
            # A cracked span on the middle bridge.
            draw.line([bx + bw // 2 - 8, y + h - 52, bx + bw // 2 + 8,
                       y + h - 36], fill=RED, width=4)


def cyclone(draw, cx, cy, r):
    """Spiral storm: concentric arcs in deep blue."""
    for k in range(5):
        rr = r * (1 - k * 0.16)
        draw.arc([cx - rr, cy - rr, cx + rr, cy + rr],
                 start=30 + k * 55, end=310 + k * 55,
                 fill=BLUE, width=7)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=RED)


def eu_stars(draw, cx, cy, r):
    """Ring of twelve gold stars on a blue disc: the EU flag, simplified."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=BLUE)
    import math
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx, sy = cx + int(0.68 * r * math.cos(a)), cy + int(0.68 * r * math.sin(a))
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=GOLD)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Double outer rule.
    d.rectangle([14, 14, W - 14, H - 14], outline=RULE, width=3)
    d.rectangle([22, 22, W - 22, H - 22], outline=RULE, width=1)

    # Masthead: different from yesterday's — short title, date as the line.
    title = "ONE DAY · ONE PAGE"
    tf = font(SERIF_B, 58)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 36), title, font=tf, fill=INK)
    d.line([40, 116, W - 40, 116], fill=RULE, width=3)
    sub = "SATURDAY 21 NOVEMBER 2026  ·  THE WORLD'S NEWS IN ONE IMAGE"
    sf = font(SANS_B, 21)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 126), sub, font=sf, fill=INK)
    d.line([40, 162, W - 40, 162], fill=RULE, width=1)

    # --- Lead: Russia's overnight barrage (full width, y 176-404) ---
    box(d, 36, 176, 952, 228)
    y = kicker(d, 52, 188, "KYIV  ·  WAR, HOURS AFTER SHENZHEN")
    y = para(d, 52, y, "Peace photo, then the missiles",
             font(SERIF_B, 38), 600, 44)
    y = para(d, 52, y + 6,
             "Russia fires 110+ missiles and 400 drones at Ukraine "
             "overnight — its biggest strike of November. At least 9 "
             "killed; three Kyiv bridges hit. Missiles crash into "
             "Poland; Warsaw calls it a deliberate provocation.",
             font(SANS, 19), 600, 23)
    bridges(d, 690, 208, 282, 168)

    # --- Row 2: Shenzhen summit | Cyclone Akvan (y 412-636) ---
    box(d, 36, 412, 466, 224)
    y = kicker(d, 52, 424, "SHENZHEN  ·  THE SUMMIT")
    y = para(d, 52, y, "Three leaders, one warning",
             font(SERIF_B, 27), 434, 33)
    y = para(d, 52, y + 6,
             "Trump, Xi and Putin declare that \"a nuclear war cannot "
             "be won and must never be fought\" and pledge talks on "
             "nuclear risks. No Ukraine or Gaza breakthrough; Trump "
             "flies home for a noon White House briefing.",
             font(SANS, 18), 434, 23)

    box(d, 522, 412, 466, 224)
    y = kicker(d, 538, 424, "ODISHA, INDIA  ·  WEATHER")
    y = para(d, 538, y, "Cyclone Akvan spares Odisha",
             font(SERIF_B, 27), 434, 33)
    y = para(d, 538, y + 6,
             "Akvan crosses near Gopalpur on Friday morning, winds "
             "70-80 km/h, then weakens fast. No deaths; 372,000 had "
             "been moved to safety.",
             font(SANS, 18), 320, 23)
    cyclone(d, 902, 560, 52)

    # --- Row 3: AI rout | UK-EU deal (y 650-880) ---
    box(d, 36, 650, 466, 230)
    y = kicker(d, 52, 662, "WALL STREET  ·  MARKETS")
    y = para(d, 52, y, "The AI rout wipes out 2026",
             font(SERIF_B, 27), 434, 33)
    d.text((52, y + 4), "NASDAQ  -5.28%", font=font(SANS_B, 34), fill=RED)
    y = para(d, 52, y + 54,
             "Nasdaq sinks 1,261 points and ends the year in the red. "
             "Anthropic falls 8.5% to $88.91, barely above its $83 "
             "IPO price; Nvidia drops 14%.",
             font(SANS, 18), 434, 23)

    box(d, 522, 650, 466, 230)
    y = kicker(d, 538, 662, "BRUSSELS  ·  BRITAIN AND EUROPE")
    y = para(d, 538, y, "UK and EU rebuild the bridge",
             font(SERIF_B, 27), 434, 33)
    y = para(d, 538, y + 6,
             "A decade after Brexit, London and Brussels agree a "
             "\"landmark\" reset: food checks scrapped, carbon markets "
             "linked, 100,000 young people each way for 3 years.",
             font(SANS, 18), 320, 23)
    eu_stars(d, 902, 790, 52)

    # --- Footer ---
    d.line([40, 894, W - 40, 894], fill=RULE, width=1)
    foot = ("Drawn early on Saturday 21 November 2026 (UTC). The barrage, "
            "the summit, the cyclone landfall, the market close and the "
            "UK-EU deal are Friday 20 November's news as reported "
            "overnight. Sources: ISW, CNN, The Times, India Meteorological "
            "Department, Wall Street Journal, Associated Press.")
    para(d, 40, 906, foot, font(SANS, 15), 944, 21, color=GREY)

    img.save("entry.png", format="PNG")
    print("wrote entry.png")


if __name__ == "__main__":
    main()
