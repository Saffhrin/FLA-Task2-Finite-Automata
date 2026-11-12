"""Build the Task 2 SVG diagrams and their local HTML gallery (stdlib only)."""
from html import escape
from pathlib import Path
from math import hypot

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "diagrams"
RADIUS = 31


def graph_svg(title, width, height, states, edges, start, note=""):
    """Render a small directed state graph as an accessible SVG."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#344054"/></marker></defs>',
        '<rect width="100%" height="100%" rx="16" fill="#fff"/>',
        '<style>text{font-family:system-ui,Segoe UI,sans-serif;fill:#172b4d}.edge{stroke:#344054;stroke-width:2;fill:none;marker-end:url(#arrow)}.node{fill:#fff;stroke:#344054;stroke-width:2}.accept{stroke:#155eef}.label{font-size:15px}.small{font-size:13px;fill:#526174}</style>',
        f'<text x="24" y="32" font-size="20" font-weight="700">{escape(title)}</text>',
    ]
    coords = {key: (x, y) for key, x, y, _label, _accept in states}
    for source, target, label, curve in edges:
        x1, y1 = coords[source]
        x2, y2 = coords[target]
        if source == target:
            d = f"M{x1-18},{y1-25} C{x1-62},{y1-90} {x1+62},{y1-90} {x1+18},{y1-25}"
            lx, ly = x1, y1 - 77
        else:
            dx, dy = x2 - x1, y2 - y1
            length = max(1.0, hypot(dx, dy))
            px, py = -dy / length, dx / length
            cx, cy = (x1 + x2) / 2 + px * curve, (y1 + y2) / 2 + py * curve
            sx, sy = cx - x1, cy - y1
            ex, ey = cx - x2, cy - y2
            sl, el = max(1.0, hypot(sx, sy)), max(1.0, hypot(ex, ey))
            ax, ay = x1 + sx / sl * RADIUS, y1 + sy / sl * RADIUS
            bx, by = x2 + ex / el * RADIUS, y2 + ey / el * RADIUS
            d = f"M{ax:.1f},{ay:.1f} Q{cx:.1f},{cy:.1f} {bx:.1f},{by:.1f}"
            lx = (ax + 2 * cx + bx) / 4
            ly = (ay + 2 * cy + by) / 4 - 7
        parts.append(f'<path class="edge" d="{d}"/>')
        label_width = max(28, len(label) * 8 + 10)
        parts.append(f'<rect x="{lx-label_width/2:.1f}" y="{ly-16:.1f}" width="{label_width}" height="21" rx="5" fill="#fff"/>')
        parts.append(f'<text class="label" text-anchor="middle" x="{lx:.1f}" y="{ly:.1f}">{escape(label)}</text>')
    sx, sy = coords[start]
    parts.append(f'<path class="edge" d="M{sx-78},{sy} L{sx-RADIUS-4},{sy}"/>')
    for key, x, y, label, accepting in states:
        cls = "node accept" if accepting else "node"
        parts.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{RADIUS}"/>')
        if accepting:
            parts.append(f'<circle cx="{x}" cy="{y}" r="{RADIUS-5}" fill="none" stroke="#155eef" stroke-width="1.5"/>')
        parts.append(f'<text text-anchor="middle" dominant-baseline="middle" x="{x}" y="{y}" font-size="16">{escape(label)}</text>')
    if note:
        notes = note if isinstance(note, (tuple, list)) else [note]
        first_y = height - 18 - 20 * (len(notes) - 1)
        for index, line in enumerate(notes):
            parts.append(f'<text class="small" x="24" y="{first_y + 20*index}">{escape(line)}</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def password_svg():
    width, height = 980, 270
    cards = [
        (30, "Length", "0 → 1 → … → 8+", "accept when 8+"),
        (220, "Uppercase", "unseen → seen", "ASCII A–Z"),
        (410, "Lowercase", "unseen → seen", "ASCII a–z"),
        (600, "Digit", "unseen → seen", "ASCII 0–9"),
        (790, "Special", "unseen → seen", "ASCII non-alphanumeric"),
    ]
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-label="Password policy product DFA">',
        '<rect width="100%" height="100%" rx="16" fill="#fff"/>',
        '<style>text{font-family:system-ui,Segoe UI,sans-serif;fill:#172b4d}.box{fill:#f8fafc;stroke:#98a2b3;stroke-width:1.5}.arrow{stroke:#344054;stroke-width:2;marker-end:url(#arr)}.muted{fill:#526174;font-size:13px}</style>',
        '<defs><marker id="arr" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="#344054"/></marker></defs>',
        '<text x="24" y="32" font-size="20" font-weight="700">Password policy: direct product of five small DFAs</text>',
    ]
    for x, title, line, detail in cards:
        parts.append(f'<rect class="box" x="{x}" y="68" width="160" height="112" rx="12"/>')
        parts.append(f'<text x="{x+80}" y="96" text-anchor="middle" font-weight="700">{escape(title)}</text>')
        parts.append(f'<text x="{x+80}" y="127" text-anchor="middle" font-size="14">{escape(line)}</text>')
        parts.append(f'<text class="muted" x="{x+80}" y="154" text-anchor="middle">{escape(detail)}</text>')
    parts.append('<text x="490" y="218" text-anchor="middle" font-size="16" font-weight="700">Accept when length = 8+ AND all four category flags are seen</text>')
    parts.append('<text class="muted" x="490" y="244" text-anchor="middle">At most 144 product states; 112 are reachable over the model’s input classes</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def password_length_svg():
    states = [(f"q{i}", 95 + i * 155, 150, f"q{i}", i == 8) for i in range(9)]
    edges = [(f"q{i}", f"q{i+1}", "Σ", 0) for i in range(8)]
    edges.append(("q8", "q8", "Σ", 0))
    return graph_svg(
        "Password length DFA (counts up to 8)", 1450, 270, states, edges, "q0",
        "Each Σ transition reads one symbol (e.g. a, 5, or !). q8 means length 8 or more and loops on Σ.")


def pin_svg():
    """Hand-route sink transitions so labels and digit edges remain distinct."""
    points = {"q0": (95, 130), "q1": (270, 130), "q2": (445, 130),
              "q3": (620, 130), "q4": (795, 130), "dead": (445, 360)}
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 455" role="img" aria-label="Four-digit PIN DFA transition diagram">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#344054"/></marker></defs>',
        '<rect width="100%" height="100%" rx="16" fill="#fff"/>',
        '<style>text{font-family:system-ui,Segoe UI,sans-serif;fill:#172b4d}.edge{fill:none;stroke:#344054;stroke-width:2;marker-end:url(#arrow)}.node{fill:#fff;stroke:#344054;stroke-width:2}.label{font-size:15px}.note{font-size:14px;fill:#526174}</style>',
        '<text x="24" y="32" font-size="20" font-weight="700">Four-digit PIN DFA</text>',
    ]
    def edge(path, label, x, y):
        width = max(34, len(label) * 8 + 10)
        parts.append(f'<path class="edge" d="{path}"/>')
        parts.append(f'<rect x="{x-width/2}" y="{y-17}" width="{width}" height="22" rx="5" fill="#fff"/>')
        parts.append(f'<text class="label" x="{x}" y="{y}" text-anchor="middle">{escape(label)}</text>')
    parts.append('<path class="edge" d="M18,130 L57,130"/>')
    for i in range(4):
        x1, y = points[f"q{i}"]
        x2, _ = points[f"q{i+1}"]
        edge(f"M{x1+32},{y} L{x2-32},{y}", "D (one digit)", (x1+x2)//2, y-14)
    # Every non-digit from q0–q3 follows a separate lower arc into the sink.
    routes = [
        ("M95,162 C105,235 315,270 418,329", "O", 155, 222),
        ("M270,162 C280,225 365,270 430,329", "O", 310, 246),
        ("M445,162 L445,325", "O", 475, 245),
        ("M620,162 C610,225 525,270 460,329", "O", 580, 246),
        ("M795,162 C785,235 575,270 472,329", "any", 735, 222),
    ]
    for path, label, x, y in routes:
        edge(path, label, x, y)
    edge("M421,338 C378,285 512,285 469,338", "any", 445, 278)
    for state, (x, y) in points.items():
        accepting = state == "q4"
        parts.append(f'<circle class="node" cx="{x}" cy="{y}" r="32" stroke="{"#155eef" if accepting else "#344054"}"/>')
        if accepting:
            parts.append(f'<circle cx="{x}" cy="{y}" r="26" fill="none" stroke="#155eef" stroke-width="1.5"/>')
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="16">{state}</text>')
    parts.append('<text class="note" x="24" y="414">D = one ASCII digit (0–9; e.g. 7); O = one non-digit character. q4 accepts at end; extra input reaches dead.</text>')
    parts.append('</svg>')
    return "\n".join(parts)


def password_flags_svg():
    """Draw the 16-state subset DFA for the four requirement flags."""
    categories = ("U", "L", "D", "S")
    colors = {"U": "#087e8b", "L": "#155eef", "D": "#7a5af8", "S": "#c4320a"}
    positions = {
        frozenset(): (690, 120),
        frozenset({"U"}): (210, 270), frozenset({"L"}): (520, 270),
        frozenset({"D"}): (860, 270), frozenset({"S"}): (1170, 270),
        frozenset({"U","L"}): (110, 430), frozenset({"U","D"}): (330, 430),
        frozenset({"U","S"}): (570, 430), frozenset({"L","D"}): (810, 430),
        frozenset({"L","S"}): (1050, 430), frozenset({"D","S"}): (1270, 430),
        frozenset({"U","L","D"}): (210, 590), frozenset({"U","L","S"}): (520, 590),
        frozenset({"U","D","S"}): (860, 590), frozenset({"L","D","S"}): (1170, 590),
        frozenset({"U","L","D","S"}): (690, 750),
    }
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1380 830" role="img" aria-label="Password category product DFA with sixteen states">',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="#344054"/></marker></defs>',
        '<rect width="100%" height="100%" rx="16" fill="#fff"/>',
        '<style>text{font-family:system-ui,Segoe UI,sans-serif;fill:#172b4d}.edge{fill:none;stroke-width:1.6;marker-end:url(#arrow)}.node{fill:white;stroke:#344054;stroke-width:2}.muted{fill:#526174;font-size:14px}</style>',
        '<text x="24" y="36" font-size="21" font-weight="700">Password category DFA: 16 seen/not-seen combinations</text>',
    ]
    parts.append('<path d="M690,65 L690,92" stroke="#344054" stroke-width="2" marker-end="url(#arrow)"/>')
    parts.append('<text class="muted" x="706" y="82">start</text>')
    sets = list(positions)
    # A transition adds a category flag; already-seen categories loop at the same state.
    for state in sets:
        x1, y1 = positions[state]
        for category in categories:
            if category in state:
                continue
            target = frozenset(set(state) | {category})
            x2, y2 = positions[target]
            dx, dy = x2 - x1, y2 - y1
            length = max(1.0, hypot(dx, dy))
            px, py = -dy / length, dx / length
            curve = (categories.index(category) - 1.5) * 8
            cx, cy = (x1+x2)/2 + px*curve, (y1+y2)/2 + py*curve
            sx, sy = cx-x1, cy-y1
            ex, ey = cx-x2, cy-y2
            sl, el = max(1.0,hypot(sx,sy)), max(1.0,hypot(ex,ey))
            ax, ay = x1+sx/sl*25, y1+sy/sl*25
            bx, by = x2+ex/el*25, y2+ey/el*25
            parts.append(f'<path class="edge" stroke="{colors[category]}" d="M{ax:.1f},{ay:.1f} Q{cx:.1f},{cy:.1f} {bx:.1f},{by:.1f}"/>')
            lx, ly = (ax+2*cx+bx)/4, (ay+2*cy+by)/4-4
            parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" font-size="13" fill="{colors[category]}">{category}</text>')
    for state, (x, y) in positions.items():
        label = "".join(category for category in categories if category in state) or "none"
        accepting = len(state) == 4
        parts.append(f'<circle class="node" cx="{x}" cy="{y}" r="25" stroke="{"#155eef" if accepting else "#344054"}"/>')
        if accepting:
            parts.append(f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="#155eef" stroke-width="1.5"/>')
        parts.append(f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-size="13">{label}</text>')
        loop_label = ",".join(["O"] + [category for category in categories if category in state])
        parts.append(f'<path d="M{x-14},{y-21} C{x-45},{y-75} {x+45},{y-75} {x+14},{y-21}" fill="none" stroke="#667085" stroke-width="1.4" marker-end="url(#arrow)"/>')
        parts.append(f'<text class="muted" x="{x}" y="{y-63}" text-anchor="middle">{loop_label} loop</text>')
    parts.extend([
        '<text class="muted" x="24" y="800">U = uppercase · L = lowercase · D = digit · S = ASCII non-alphanumeric · O = non-ASCII (category-neutral); seen categories loop.</text>',
        '<text class="muted" x="24" y="821">The full password product also tracks length; acceptance requires q8 (8+) and the accepting ULDS state.</text>',
        '</svg>',
    ])
    return "\n".join(parts)


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    diagrams = {
        "password_product.svg": password_svg(),
        "password_length_dfa.svg": password_length_svg(),
        "password_category_dfa.svg": password_flags_svg(),
        "pin_dfa.svg": pin_svg(),
        "session_lockout.svg": graph_svg(
            "Three-consecutive-failure session DFA", 970, 350,
            [("READY", 130, 190, "READY", False), ("ONE", 365, 190, "ONE", False),
             ("TWO", 600, 190, "TWO", False), ("LOCKED", 835, 190, "LOCKED", False)],
            [("READY", "READY", "C", 0), ("READY", "ONE", "W", 0),
             ("ONE", "READY", "C", -72), ("ONE", "TWO", "W", 0),
             ("TWO", "READY", "C", -130), ("TWO", "LOCKED", "W", 0),
             ("LOCKED", "LOCKED", "C or W", 0)], "READY",
            "C = correct attempt (reset); W = wrong attempt; LOCKED is absorbing."),
        "email_nfa.svg": graph_svg(
            "Email-format NFA (declared ASCII subset)", 1450, 680,
            [("ls", 100, 220, "n0", False), ("lw", 310, 220, "n1", False),
             ("ln", 310, 430, "n2", False), ("ds", 520, 220, "n3", False),
             ("dw", 730, 220, "n4", False), ("da", 970, 220, "n6", False),
             ("dn", 730, 430, "n5", False), ("tf", 970, 430, "n7", False),
             ("to", 1180, 430, "n8", False), ("ta", 1350, 220, "n9", True)],
            [("ls", "lw", "A", 0), ("lw", "lw", "A", 0),
             ("lw", "ln", "sep", 50), ("ln", "lw", "A", 50),
             ("lw", "ds", "@", 0), ("ds", "dw", "A", 0),
             ("dw", "dw", "A", 0), ("dw", "dn", "-", 50),
             ("dn", "dw", "A", 50), ("dw", "da", ".", 0),
             ("dw", "tf", ".", 0), ("da", "dw", "A", 50),
             ("tf", "to", "letter", 0), ("to", "ta", "letter", -45),
             ("ta", "ta", "letter", 0)], "ls",
            ("A = one ASCII letter/digit; letter = one ASCII letter; sep = one local separator (._-).",
             "At a domain dot the NFA branches: continue another label, or guess the suffix begins.",
             "n0 local start · n1 local part · n2 after local separator · n3 after @ · n4 domain label",
             "n5 after domain hyphen · n6 after domain dot · n7/n8 suffix characters · n9 accepting")),
    }
    for filename, svg in diagrams.items():
        (OUTPUT / filename).write_text(svg + "\n", encoding="utf-8")

    descriptions = {
        "password_product.svg": "A capped length counter and four independent seen/not-seen DFAs combine by direct product.",
        "password_length_dfa.svg": "The length component counts up to eight; its final state represents every length of eight or more.",
        "password_category_dfa.svg": "The 16-state category-flag DFA shows the accepting combination and category transitions.",
        "pin_dfa.svg": "Four ASCII digits are consumed in sequence; invalid and extra input is rejected.",
        "session_lockout.svg": "Correct attempts reset the streak; three consecutive failures lock the session.",
        "email_nfa.svg": "A domain dot creates two NFA paths so the final suffix can be guessed nondeterministically.",
    }
    cards = []
    for filename, description in descriptions.items():
        title = filename.removesuffix(".svg").replace("_", " ").title()
        cards.append(
            '<article class="card">'
            f'<h2>{escape(title)}</h2><p>{escape(description)}</p>'
            f'<a href="{escape(filename)}"><img src="{escape(filename)}" alt="{escape(title)} state diagram"></a>'
            '</article>'
        )
    template = (ROOT / "tools" / "demo_template.html").read_text(encoding="utf-8")
    gallery = template.replace("{{DIAGRAM_CARDS}}", "\n".join(cards))
    (OUTPUT / "index.html").write_text(gallery, encoding="utf-8")
    print(f"Wrote {len(diagrams)} SVG diagrams and {OUTPUT / 'index.html'}")


if __name__ == "__main__":
    build()
