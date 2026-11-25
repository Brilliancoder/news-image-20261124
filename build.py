"""Build-time renderer for entry.png (make.fun news-image-20261124).

Needs Pillow and the Noto fonts; run `python3 build.py`. main.py only copies the result.
Every story below was checked against reporting dated 24 Nov 2026 (see README.md).
"""
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample factor
W = H = 1024
NOTO = '/usr/share/fonts/truetype/noto/'

PAPER, CARD, INK, GREY = '#f3efe6', '#fffefa', '#141414', '#4a4a4a'
NAVY, GOLD = '#0f2240', '#f2a93b'
TAG = {  # category colours, also used for map pins
    'conflict': '#c0392b', 'politics': '#2b5797', 'business': '#1e8449',
    'science': '#138d9c', 'sport': '#d35400', 'society': '#8e6c1a',
}

_fonts = {}


def sans(weight, px):
    key = (weight, px)
    if key not in _fonts:
        name = 'NotoSans-Condensed' + ('' if weight == 'Regular' else weight) + '.ttf'
        _fonts[key] = ImageFont.truetype(NOTO + name, round(px * S))
    return _fonts[key]


def serif(px):
    return ImageFont.truetype(NOTO + 'NotoSerif-CondensedBlack.ttf', round(px * S))


img = Image.new('RGB', (W * S, H * S), PAPER)
d = ImageDraw.Draw(img, 'RGBA')


def sc(pts):
    return [(x * S, y * S) for x, y in pts]


def rect(x0, y0, x1, y1, fill=None, outline=None, width=1, r=0):
    d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill,
                        outline=outline, width=round(width * S))


def circle(x, y, r, fill=None, outline=None, width=1):
    d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill,
              outline=outline, width=round(width * S))


def poly(pts, fill, outline=None):
    d.polygon(sc(pts), fill=fill, outline=outline)


def line(pts, fill, width):
    d.line(sc(pts), fill=fill, width=round(width * S), joint='curve')


def text(x, y, s, font, fill=INK, anchor='la'):
    d.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)


def tw(s, font):
    return d.textlength(s, font=font) / S


def wrap(s, font, width):
    lines, cur = [], ''
    for word in s.split():
        trial = (cur + ' ' + word).strip()
        if tw(trial, font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    return lines + [cur]


def block(x, y, s, weight, px, width, max_lines, fill=INK, lead=1.18):
    """Draw wrapped text, shrinking the size until it fits max_lines; returns the bottom y."""
    while True:
        f = sans(weight, px)
        lines = wrap(s, f, width)
        if len(lines) <= max_lines or px <= 9:
            break
        px -= 0.5
    assert len(lines) <= max_lines, s  # never silently drop text
    for i, ln in enumerate(lines):
        text(x, y + i * px * lead, ln, f, fill)
    return y + len(lines) * px * lead


# ---------------------------------------------------------------- stories
# (number, tag, kicker, headline, deck, lon, lat)
HEROES = [
    (1, 'business', 'USA · WALL STREET', 'AI stocks slide; Nvidia falls 5.9%',
     'A day after its 31% jump on Jensen Huang\'s return, Nvidia closes at $155.38. Nasdaq -1.5%, Dow +0.9%.',
     -74, 40.7),
    (2, 'politics', 'USA · CHINA · COURTS', 'US jury finds Huawei guilty',
     'Brooklyn jury convicts on 10 of 12 counts, incl. trade-secret theft conspiracy and bank fraud; cleared of racketeering.',
     -74, 40.7),
    (3, 'conflict', 'IRAN · GULF', 'Iran says 4th tanker hit mine in Hormuz',
     'IRGC claim, not independently verified: mine blasts hit tankers despite US naval escort; it warns shippers.',
     56.3, 26.5),
    (4, 'conflict', 'GAZA', 'Israel kills Hamas internal security chief',
     'Naeem Abu Nahel and six others die in a strike in Gaza City, medics say, despite the October ceasefire.',
     34.45, 31.5),
]

GRID = [
    (5, 'business', 'USA · MARKETS', 'Anthropic falls below IPO price',
     'Closes at $81.91, under its $83 offer, four sessions after its record listing.', -74, 40.7),
    (6, 'conflict', 'UKRAINE · BALTIC', 'Kyiv confirms Baltic ship strike',
     'Zelensky confirms drone hit on Russian cargo ship in Gulf of Finland; Norway urges caution.', 28, 60),
    (7, 'politics', 'HUNGARY · UKRAINE', 'Magyar meets Zelensky',
     'First formal talks, in Uzhhorod; Hungary\'s PM hails "a historic day" after Orban era.', 22.3, 48.6),
    (8, 'conflict', 'UKRAINE', 'Strike on Zaporizhzhia kills 2',
     'Overnight Russian attack on an apartment block wounds about 40, incl. 4 children.', 35.1, 47.8),
    (9, 'conflict', 'SOUTH KOREA · RUSSIA', 'Russian jets near Ulleungdo',
     'Bombers enter air defence zone; Seoul scrambles F-15Ks, sends shelter alert, protests.', 130.9, 37.5),
    (10, 'politics', 'NORTH KOREA', 'Kim Yo Jong turns on Switzerland',
     'Says Pyongyang must rethink ties after Swiss sanctions on a youth camp.', 125.8, 39),
    (11, 'conflict', 'YEMEN', 'Houthis 60 km from Aden',
     'Army says the rebels are "ready to attack" but will not take the city.', 45, 12.8),
    (12, 'conflict', 'SAUDI ARABIA', 'Drone hits Riyadh\'s PIF Tower',
     'Civil defence blames Houthis; 11 hurt in second attack in under a week.', 46.7, 24.7),
    (13, 'society', 'GAZA', 'Meningitis epidemic alert in Gaza',
     'Health ministry: 272 cases in October, over 8x the usual monthly rate.', 34.3, 31.3),
    (14, 'politics', 'LIBYA · TURKIYE', 'Haftar\'s first visit to Turkey',
     'Eastern Libya commander arrives in Ankara at Erdogan\'s invitation.', 32.9, 39.9),
    (15, 'society', 'TURKIYE', 'Army helicopter crash kills 5',
     'AS-532 goes down on a training flight in Eskisehir province.', 30.5, 39.8),
    (16, 'society', 'VIETNAM', 'Hanoi restaurant blast kills 6+',
     'Suspected gas explosion wrecks a hot-pot eatery; over a dozen hurt.', 105.8, 21),
    (17, 'politics', 'MALAYSIA · MYANMAR', 'Malaysia to send 6,803 home',
     'Anwar: Myanmar nationals go back in December, days after ICJ genocide ruling.', 101.7, 3.1),
    (18, 'politics', 'BANGLADESH', 'Hasina plans return on Dec 16',
     'Ex-PM, sentenced to death in absentia, asks to be flown to Dhaka.', 90.4, 23.8),
    (19, 'politics', 'JAPAN', 'Japan to pay ICC dues early',
     'PM Takaichi pledges full 2027 contribution before US sanctions bite.', 139.7, 35.7),
    (20, 'science', 'CHINA · PAKISTAN · SPACE', 'Shenzhou-24 lifts off',
     'Launch 19:18 EST Tue takes Pakistan\'s Zeeshan Ali, first foreign astronaut, to Tiangong.',
     100.3, 40.9),
    (21, 'society', 'COLOMBIA', 'Hostages held in Cartagena store',
     'Gunmen flee failed heist into supermarket; about 25 held, airport briefly halted.', -75.5, 10.4),
    (22, 'society', 'CUBA · WHO', 'WHO pledges $2m to Cuba',
     'Tedros ends visit to a health system short of vaccines and supplies.', -82.4, 23.1),
    (23, 'politics', 'ETHIOPIA', 'Amnesty urges Tigray probe',
     'Calls for war-crimes inquiry into shelling of towns this year.', 39.5, 13.5),
    (24, 'sport', 'FOOTBALL · EUROPE', 'Real Madrid thrash PSV 5-1',
     'Champions League: Man City 2-2 Napoli, Arsenal 1-1 Dortmund.', -3.7, 40.4),
]

NUMBERS = [
    ('-5.86%', 'Nvidia close, Tuesday'),
    ('$81.91', 'Anthropic close (IPO $83)'),
    ('10 of 12', 'counts Huawei convicted on'),
    ('6,803', 'Myanmar nationals to be sent back'),
    ('60 km', 'Houthis from Aden, army says'),
]

# ---------------------------------------------------------------- header
rect(0, 0, W, 98, fill=NAVY)
rect(0, 98, W, 103, fill=GOLD)
text(24, 15, 'WORLD NEWS IN ONE PAGE  ·  24 STORIES ACROSS 5 CONTINENTS', sans('Bold', 15), GOLD)
text(22, 36, 'TUESDAY 24 NOVEMBER 2026', serif(48), '#ffffff')
text(W - 24, 22, 'One day, as reported', sans('Bold', 19), GOLD, 'ra')
text(W - 24, 50, 'Events that happened or were first', sans('Regular', 14), '#d8deea', 'ra')
text(W - 24, 68, 'reported on 24 Nov 2026', sans('Regular', 14), '#d8deea', 'ra')


# ---------------------------------------------------------------- hero art
def art_market(x, y, w, h):
    rect(x, y, x + w, y + h, fill='#13202f')
    for i in range(1, 6):
        line([(x, y + i * h / 6), (x + w, y + i * h / 6)], '#ffffff18', 1)
    pts = [(x + 12, y + 92), (x + 50, y + 70), (x + 85, y + 28), (x + 120, y + 18),
           (x + 150, y + 52), (x + 180, y + 66), (x + 212, y + 98)]
    line(pts, '#e74c3c', 4)
    poly([(x + 202, y + 104), (x + 226, y + 108), (x + 220, y + 84)], '#e74c3c')
    text(x + 16, y + 14, 'NVDA', sans('Black', 22), '#ffffff')
    text(x + 16, y + 40, '-5.9%', sans('Black', 30), '#ff6b5b')


def art_court(x, y, w, h):
    rect(x, y, x + w, y + h, fill='#dfe6ef')
    cx = x + w / 2
    poly([(cx - 78, y + 40), (cx, y + 12), (cx + 78, y + 40)], '#2b5797')
    rect(cx - 80, y + 40, cx + 80, y + 47, fill='#2b5797')
    for i in range(5):
        px = cx - 64 + i * 32
        rect(px - 6, y + 50, px + 6, y + 94, fill='#ffffff', outline='#2b5797', width=1.5)
    rect(cx - 86, y + 96, cx + 86, y + 104, fill='#2b5797')
    text(cx, y + 31, 'GUILTY', sans('Black', 13), '#ffffff', 'mm')
    rect(x + 8, y + h - 26, x + 92, y + h - 8, fill='#c0392b', r=3)
    text(x + 50, y + h - 17, 'HUAWEI', sans('Black', 12), '#ffffff', 'mm')


def art_tanker(x, y, w, h):
    rect(x, y, x + w, y + h, fill='#f6c47a')
    rect(x, y + 72, x + w, y + h, fill='#245b7a')
    poly([(x + 40, y + 62), (x + 190, y + 62), (x + 176, y + 84), (x + 52, y + 84)], '#2d2d2d')
    rect(x + 160, y + 44, x + 182, y + 62, fill='#f4f4f4')
    for i, (dx, r) in enumerate([(0, 14), (14, 18), (32, 22)]):
        circle(x + 90 + dx, y + 46 - i * 14, r, fill='#3a3a3acc')
    circle(x + 92, y + 64, 9, fill='#ff7b1a')
    circle(x + 92, y + 64, 4, fill='#ffe27a')
    circle(x + 205, y + 100, 8, fill='#1a1a1a')
    for a, b in [(-11, 0), (11, 0), (0, -11), (0, 11)]:
        line([(x + 205, y + 100), (x + 205 + a, y + 100 + b)], '#1a1a1a', 2)


def art_gaza(x, y, w, h):
    rect(x, y, x + w, y + h, fill='#d9c3a0')
    for i, (bw, bh) in enumerate([(26, 40), (20, 58), (30, 34), (22, 64), (28, 44), (24, 52), (30, 38), (22, 48)]):
        bx = x + 6 + i * 29
        rect(bx, y + h - bh, bx + bw, y + h, fill='#5b4a3a')
    for dx, dy, r in [(0, 0, 16), (-12, -16, 14), (10, -28, 18), (-4, -46, 20)]:
        circle(x + 130 + dx, y + 58 + dy, r, fill='#4d4d4dcc')
    circle(x + 130, y + 70, 9, fill='#ff7b1a')


ART = [art_market, art_court, art_tanker, art_gaza]

# ---------------------------------------------------------------- hero cards
CW, GAP, X0, HY = 241, 10, 12, 113
for i, (n, tag, kick, head, deck, _, _) in enumerate(HEROES):
    x = X0 + i * (CW + GAP)
    rect(x, HY, x + CW, 392, fill=CARD, outline='#d6cfbf')
    ART[i](x + 1, HY + 1, CW - 2, 118)
    rect(x + 1, HY + 119, x + CW - 1, HY + 123, fill=TAG[tag])
    circle(x + CW - 17, HY + 17, 12, fill=INK)
    text(x + CW - 17, HY + 17, str(n), sans('Black', 14), '#ffffff', 'mm')
    text(x + 12, HY + 132, kick, sans('Bold', 12.5), TAG[tag])
    yb = block(x + 12, HY + 151, head, 'ExtraBold', 23, CW - 24, 2, INK, 1.12)
    block(x + 12, yb + 6, deck, 'Regular', 13.5, CW - 24, 4, GREY, 1.22)

# ---------------------------------------------------------------- world map
MX0, MY0, MX1, MY1 = 12, 402, 660, 606
rect(MX0, MY0, MX1, MY1, fill='#d6e6f0', outline='#b8cbd8')


def proj(lon, lat):
    # equirectangular crop: lon -125..150, lat 68..-38
    return (MX0 + (lon + 125) / 275 * (MX1 - MX0), MY0 + (68 - lat) / 106 * (MY1 - MY0))


LAND = [  # rough hand-drawn continent outlines (lon, lat)
    [(-125, 49), (-123, 60), (-110, 68), (-85, 68), (-78, 62), (-65, 60), (-55, 50), (-70, 43),
     (-76, 35), (-81, 25), (-90, 29), (-97, 26), (-97, 19), (-88, 15), (-83, 9), (-79, 8),
     (-92, 15), (-105, 20), (-112, 29), (-117, 33), (-124, 41)],
    [(-79, 8), (-72, 12), (-62, 10), (-50, 0), (-35, -5), (-38, -15), (-48, -26), (-57, -36),
     (-65, -38), (-73, -38), (-71, -20), (-81, -5), (-78, 2)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (3, 51), (8, 54), (5, 58), (12, 64), (22, 68),
     (40, 68), (60, 68), (80, 68), (110, 68), (140, 66), (150, 60), (142, 52), (135, 43),
     (128, 35), (122, 30), (121, 24), (110, 20), (106, 10), (100, 13), (98, 8), (103, 1),
     (98, 16), (92, 22), (88, 21), (80, 15), (77, 8), (72, 20), (66, 25), (57, 25), (52, 27),
     (48, 30), (50, 26), (56, 24), (59, 22), (52, 16), (44, 12), (42, 16), (35, 28), (34, 31),
     (36, 36), (30, 36), (26, 40), (23, 37), (20, 40), (16, 38), (12, 44), (8, 44), (3, 42), (0, 38)],
    [(-17, 15), (-16, 22), (-10, 30), (-6, 35), (10, 37), (20, 31), (32, 31), (35, 28), (43, 12),
     (51, 11), (40, -5), (40, -15), (35, -25), (27, -34), (19, -34), (12, -18), (13, -5), (9, 4),
     (-8, 4), (-15, 10)],
    [(114, -22), (122, -18), (131, -12), (137, -12), (142, -11), (146, -19), (153, -26),
     (150, -37), (140, -38), (129, -32), (115, -34)],
    [(95, 5), (105, -6), (115, -8), (118, -3), (110, 2), (104, 0)],
    [(130, 33), (135, 35), (141, 41), (142, 45), (140, 36), (133, 33)],
    [(-5, 50), (2, 52), (-3, 58), (-6, 56)],
]
for shape in LAND:
    poly([proj(*p) for p in shape], '#e2d3b3', '#b39f74')

rect(MX0 + 8, MY0 + 8, MX0 + 152, MY0 + 30, fill=NAVY, r=3)
text(MX0 + 16, MY0 + 12, 'WHERE IT HAPPENED', sans('Bold', 14), '#ffffff')

placed = []
for n, tag, *_, lon, lat in HEROES + GRID:
    px, py = proj(lon, lat)
    # nudge pins that share a spot so every number stays readable
    step = 0
    while any(abs(px - qx) < 15 and abs(py - qy) < 15 for qx, qy in placed):
        px += 16 if step % 2 == 0 else -32  # alternate right / left of the true spot
        step += 1
        if step % 2 == 0:
            px += 16
            py += 15
    placed.append((px, py))
    circle(px, py, 8, fill=TAG[tag], outline='#ffffff', width=1.5)
    text(px, py, str(n), sans('Bold', 9 if n > 9 else 10), '#ffffff', 'mm')

lx, ly = MX0 + 10, MY1 - 88
rect(lx, ly, lx + 82, MY1 - 8, fill='#ffffffd9', r=3)
for i, tag in enumerate(TAG):
    circle(lx + 10, ly + 9 + i * 12.5, 4.5, fill=TAG[tag])
    text(lx + 19, ly + 9 + i * 12.5, tag.capitalize(), sans('SemiBold', 11), INK, 'lm')

# ---------------------------------------------------------------- numbers box
NX0, NX1 = 670, W - 12
rect(NX0, MY0, NX1, MY1, fill=NAVY)
text(NX0 + 14, MY0 + 10, 'THE DAY IN NUMBERS', sans('Bold', 15), GOLD)
for i, (big, small) in enumerate(NUMBERS):
    yy = MY0 + 34 + i * 34
    if i:
        line([(NX0 + 14, yy - 3), (NX1 - 14, yy - 3)], '#ffffff30', 1)
    text(NX0 + 14, yy + 15, big, sans('Black', 23), GOLD, 'lm')
    text(NX0 + 128, yy + 15, small, sans('Medium', 13.5), '#ffffff', 'lm')

# ---------------------------------------------------------------- grid
GY0, ROWH, COLW = 613, 76, 245
for k, (n, tag, kick, head, deck, _, _) in enumerate(GRID):
    col, row = k % 4, k // 4
    x, y = X0 + col * (COLW + 4), GY0 + row * (ROWH + 2)
    rect(x, y, x + COLW, y + ROWH, fill=CARD, outline='#ddd6c6')
    rect(x, y, x + 4, y + ROWH, fill=TAG[tag])
    text(x + 12, y + 6, f'{n}  {kick}', sans('Bold', 11), TAG[tag])
    yb = block(x + 12, y + 20, head, 'ExtraBold', 17, COLW - 20, 1, INK)
    block(x + 12, yb + 2, deck, 'Regular', 12.5, COLW - 20, 2, GREY, 1.15)

text(W / 2, H - 9, 'Sources: Reuters · AP · AFP · Al Jazeera · CNBC · Bloomberg · Just Security · '
     'Yonhap · Euronews · WHO · UEFA  —  full list in README', sans('Medium', 11), GREY, 'mm')

img.resize((W, H), Image.LANCZOS).save('entry.png', optimize=True)
print('wrote entry.png')
