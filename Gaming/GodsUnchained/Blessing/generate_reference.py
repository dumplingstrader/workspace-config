"""Generate blessings.png and blessings.pdf from the table data."""

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BLESSINGS = [
    ("Balanced Blessing",    "Gain 6 favor. Then the player with the least favor gains 3 favor."),
    ("Beggar's Blessing",    "Each player with less than 12 favor has their favor set to 12."),
    ("Borrowed Blessing",    "You gain 4 favor. Your opponent loses 4 favor."),
    ("Costly Blessing",      "Each player gains 2 favor for each unlocked mana gem they have."),
    ("Damaging Blessing",    "Your opponent gains 9 favor. Deal 3 damage to their god."),
    ("Draining Blessing",    "Gain 9 favor. Deal 3 damage to your god."),
    ("Equality Blessing",    "Combine both players' favor, then evenly divide it between you (rounding up)."),
    ("Gamekeeper's Blessing","Replace visible Sanctum cards with a 1/1 Avraxus, the Gamekeeper, favor cost 10."),
    ("Greedy Blessing",      'Give a creature "At the start of your turn, if you have at least 30 favor, draw two cards."'),
    ("Growing Blessing",     'Give a creature "At the start of your turn, gain 3 favor."'),
    ("Hoarder's Blessing",   "Gain 2 favor for each card in your hand."),
    ("Inflative Blessing",   "Increase by 6 the favor cost of the visible cards in the Sanctum."),
    ("Lost Blessing",        "Your opponent loses 6 favor."),
    ("Miserly Blessing",     "Reduce by 6 the favor cost of the visible cards in the Sanctum."),
    ("Mixed Blessing",       "Shuffle the Sanctum decks. Gain 3 favor."),
    ("Simple Blessing",      "Gain 6 favor."),
    ("Stable Blessing",      "Set the favor cost of each visible Sanctum card to 20."),
    ("Trader's Blessing",    "Swap the highest and lowest favor costs of the visible cards in the Sanctum."),
    ("Triumphant Blessing",  "Each player gains 9 favor."),
    ("Zombie's Blessing",    'Summon a 1/1 Zombie with leech. Give it "At the end of your turn, gain 2 favor."'),
]

SOURCE_IMAGES = [
    ("BlessingONE.png",   "Stable Blessing, Zombie's Blessing, Borrowed Blessing"),
    ("BlessingTWO.png",   "Simple Blessing, Balanced Blessing, Gamekeeper's Blessing"),
    ("BlessingTHREE.png", "Trader's Blessing, Simple Blessing, Hoarder's Blessing"),
    ("BlessingFOUR.png",  "Damaging Blessing, Draining Blessing, Costly Blessing"),
    ("BlessingFIVE.png",  "Equality Blessing, Damaging Blessing, Beggar's Blessing"),
    ("BlessingSix.png",   "Lost Blessing, Trader's Blessing, Greedy Blessing"),
    ("BlessingSEVEN.png", "Triumphant Blessing, Hoarder's Blessing, Stable Blessing"),
    ("BlessingEIGHT.png", "Lost Blessing, Mixed Blessing, Growing Blessing"),
]

# ---------------------------------------------------------------------------
# PNG
# ---------------------------------------------------------------------------

FONT_REG  = "C:/Windows/Fonts/calibri.ttf"
FONT_BOLD = "C:/Windows/Fonts/calibrib.ttf"

WHITE      = (255, 255, 255)
LIGHT_GRAY = (248, 248, 250)
BORDER_CLR = (210, 210, 215)
HEADER_BG  = (235, 235, 240)
DARK       = (30,  30,  35)
BLUE       = (30,  80, 200)

WIDTH   = 960
PADDING = 48
COL1_W  = 220
COL2_X  = PADDING + COL1_W + 16
COL2_W  = WIDTH - COL2_X - PADDING
LINE_H  = 20


def _fonts(size=14):
    try:
        return (ImageFont.truetype(FONT_BOLD, size),
                ImageFont.truetype(FONT_REG,  size))
    except OSError:
        f = ImageFont.load_default()
        return f, f


def _wrap(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        candidate = (cur + " " + word).strip()
        w = draw.textlength(candidate, font=font)
        if w <= max_w:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines or [""]


def _row_height(draw, effect, font, max_w, base=24, pad=6):
    lines = _wrap(draw, effect, font, max_w)
    return max(base, len(lines) * LINE_H + pad * 2)


def _build_png():
    probe = Image.new("RGB", (1, 1))
    pdraw = ImageDraw.Draw(probe)

    fb14, fr14 = _fonts(14)
    fb12, fr12 = _fonts(12)
    fb24, _    = _fonts(24)
    fb18, _    = _fonts(18)

    # Calculate total height
    y = PADDING
    y += 40  # title
    y += 12
    y += 28  # h2
    y += 16
    y += 30  # table header
    for _, effect in BLESSINGS:
        y += _row_height(pdraw, effect, fr14, COL2_W)
    y += 32  # section gap
    y += 28  # source h2
    y += 12
    y += 30  # source header
    for _, cards in SOURCE_IMAGES:
        y += _row_height(pdraw, cards, fr12, COL2_W + 40)
    y += PADDING

    img  = Image.new("RGB", (WIDTH, y), WHITE)
    draw = ImageDraw.Draw(img)

    cy = PADDING

    # Title
    draw.text((PADDING, cy), "Gods Unchained — Blessing Cards", font=fb24, fill=DARK)
    cy += 40

    # H2
    cy += 8
    draw.text((PADDING, cy), f"Unique Blessings ({len(BLESSINGS)} total)", font=fb18, fill=DARK)
    cy += 32

    table_x = PADDING
    table_w = WIDTH - 2 * PADDING

    def draw_row(y_, name, effect, name_color, bg, font_name, font_effect, is_header=False):
        rh = _row_height(draw, effect, font_effect, COL2_W) if not is_header else 30
        draw.rectangle([table_x, y_, table_x + table_w, y_ + rh], fill=bg, outline=BORDER_CLR)
        draw.line([table_x + COL1_W, y_, table_x + COL1_W, y_ + rh], fill=BORDER_CLR)
        draw.text((table_x + 8, y_ + 6), name, font=font_name, fill=name_color)
        lines = _wrap(draw, effect, font_effect, COL2_W) if not is_header else [effect]
        for i, line in enumerate(lines):
            draw.text((COL2_X, y_ + 6 + i * LINE_H), line, font=font_effect, fill=DARK)
        return rh

    # Header
    cy += draw_row(cy, "Name", "Effect", DARK, HEADER_BG, fb14, fb14, is_header=True)

    # Blessing rows
    for idx, (name, effect) in enumerate(BLESSINGS):
        bg = WHITE if idx % 2 == 0 else LIGHT_GRAY
        cy += draw_row(cy, name, effect, BLUE, bg, fb14, fr14)

    cy += 32

    # Source Images section
    draw.text((PADDING, cy), "Source Images", font=fb18, fill=DARK)
    cy += 32

    src_col2_x = PADDING + 180 + 16
    src_col2_w = WIDTH - src_col2_x - PADDING

    def draw_src_row(y_, fname, cards, bg, font_f, font_c):
        rh = _row_height(draw, cards, font_c, src_col2_w)
        draw.rectangle([table_x, y_, table_x + table_w, y_ + rh], fill=bg, outline=BORDER_CLR)
        draw.line([table_x + 180, y_, table_x + 180, y_ + rh], fill=BORDER_CLR)
        draw.text((table_x + 8, y_ + 6), fname, font=font_f, fill=BLUE)
        lines = _wrap(draw, cards, font_c, src_col2_w)
        for i, line in enumerate(lines):
            draw.text((src_col2_x, y_ + 6 + i * LINE_H), line, font=font_c, fill=DARK)
        return rh

    cy += draw_row(cy, "File", "Cards", DARK, HEADER_BG, fb12, fb12, is_header=True)
    for idx, (fname, cards) in enumerate(SOURCE_IMAGES):
        bg = WHITE if idx % 2 == 0 else LIGHT_GRAY
        cy += draw_src_row(cy, fname, cards, bg, fr12, fr12)

    out = os.path.join(OUT_DIR, "blessings.png")
    img.save(out, "PNG")
    print(f"  Saved {out}")


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------

def _build_pdf():
    out  = os.path.join(OUT_DIR, "blessings.pdf")
    doc  = SimpleDocTemplate(out, pagesize=A4,
                             leftMargin=2*cm, rightMargin=2*cm,
                             topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    blue_style = ParagraphStyle("blue", parent=styles["Normal"],
                                textColor=colors.HexColor("#1e50c8"), fontSize=10)
    normal10   = ParagraphStyle("n10", parent=styles["Normal"], fontSize=10)
    normal9    = ParagraphStyle("n9",  parent=styles["Normal"], fontSize=9)
    blue9      = ParagraphStyle("b9",  parent=styles["Normal"],
                                textColor=colors.HexColor("#1e50c8"), fontSize=9)

    story = []

    # Title
    story.append(Paragraph("<b>Gods Unchained — Blessing Cards</b>",
                            ParagraphStyle("title", parent=styles["Heading1"], fontSize=20)))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(f"<b>Unique Blessings ({len(BLESSINGS)} total)</b>",
                            ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14)))
    story.append(Spacer(1, 0.2*cm))

    # Blessings table
    col1 = 5.5*cm
    col2 = A4[0] - 4*cm - col1
    data = [[Paragraph("<b>Name</b>", normal10), Paragraph("<b>Effect</b>", normal10)]]
    for name, effect in BLESSINGS:
        data.append([Paragraph(name, blue_style), Paragraph(effect, normal10)])

    t = Table(data, colWidths=[col1, col2])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8ec")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8f8fa")]),
        ("GRID",      (0, 0), (-1, -1), 0.5, colors.HexColor("#d2d2d7")),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.6*cm))

    # Source Images section
    story.append(Paragraph("<b>Source Images</b>",
                            ParagraphStyle("h2b", parent=styles["Heading2"], fontSize=14)))
    story.append(Spacer(1, 0.2*cm))

    fcol = 4.5*cm
    ccol = A4[0] - 4*cm - fcol
    sdata = [[Paragraph("<b>File</b>", normal9), Paragraph("<b>Cards</b>", normal9)]]
    for fname, cards in SOURCE_IMAGES:
        sdata.append([Paragraph(fname, blue9), Paragraph(cards, normal9)])

    st = Table(sdata, colWidths=[fcol, ccol])
    st.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8e8ec")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1),
         [colors.white, colors.HexColor("#f8f8fa")]),
        ("GRID",      (0, 0), (-1, -1), 0.5, colors.HexColor("#d2d2d7")),
        ("VALIGN",    (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING",    (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING",   (0, 0), (-1, -1), 6),
    ]))
    story.append(st)

    doc.build(story)
    print(f"  Saved {out}")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Generating blessings.png ...")
    _build_png()
    print("Generating blessings.pdf ...")
    _build_pdf()
    print("Done.")
