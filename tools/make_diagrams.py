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
        parts.append(f'<text class="small" x="24" y="{height-20}">{escape(note)}</text>')
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


def build():
    OUTPUT.mkdir(parents=True, exist_ok=True)
    diagrams = {
        "password_product.svg": password_svg(),
        "pin_dfa.svg": graph_svg(
            "Four-digit PIN DFA", 900, 260,
            [("q0", 105, 130, "q0", False), ("q1", 260, 130, "q1", False),
             ("q2", 415, 130, "q2", False), ("q3", 570, 130, "q3", False),
             ("q4", 725, 130, "q4", True), ("dead", 810, 220, "dead", False)],
            [("q0", "q1", "digit", 0), ("q1", "q2", "digit", 0),
             ("q2", "q3", "digit", 0), ("q3", "q4", "digit", 0),
             ("dead", "dead", "any", 0)], "q0",
            "Any non-digit, or any character after q4, enters the rejecting sink."),
        "session_lockout.svg": graph_svg(
            "Three-consecutive-failure session DFA", 970, 350,
            [("READY", 130, 190, "READY", False), ("ONE", 365, 190, "ONE", False),
             ("TWO", 600, 190, "TWO", False), ("LOCKED", 835, 190, "LOCKED", True)],
            [("READY", "READY", "C", 0), ("READY", "ONE", "W", 0),
             ("ONE", "READY", "C", -72), ("ONE", "TWO", "W", 0),
             ("TWO", "READY", "C", -130), ("TWO", "LOCKED", "W", 0),
             ("LOCKED", "LOCKED", "C or W", 0)], "READY",
            "C = correct attempt (reset); W = wrong attempt; LOCKED is absorbing."),
        "email_nfa.svg": graph_svg(
            "Email-format NFA (declared ASCII subset)", 1100, 500,
            [("ls", 85, 205, "local_start", False), ("lw", 235, 205, "local_word", False),
             ("ln", 235, 365, "local_need", False), ("ds", 390, 205, "domain_start", False),
             ("dw", 550, 205, "domain_word", False), ("da", 720, 205, "after_dot", False),
             ("dn", 550, 365, "domain_need", False), ("tf", 720, 365, "tld_first", False),
             ("to", 900, 365, "tld_one", False), ("ta", 1030, 205, "tld_accept", True)],
            [("ls", "lw", "alnum", 0), ("lw", "lw", "alnum", 0),
             ("lw", "ln", "._-", 0), ("ln", "lw", "alnum", 0),
             ("lw", "ds", "@", 0), ("ds", "dw", "alnum", 0),
             ("dw", "dw", "alnum", 0), ("dw", "dn", "-", 0),
             ("dn", "dw", "alnum", 0), ("dw", "da", ". continue", 0),
             ("dw", "tf", ". suffix", 0), ("da", "dw", "alnum", 0),
             ("tf", "to", "letter", 0), ("to", "ta", "letter", 0),
             ("ta", "ta", "letter", 0)], "ls",
            "At a domain dot, the NFA branches: continue a label or guess the suffix begins."),
    }
    for filename, svg in diagrams.items():
        (OUTPUT / filename).write_text(svg + "\n", encoding="utf-8")

    descriptions = {
        "password_product.svg": "A capped length counter and four independent seen/not-seen DFAs combine by direct product.",
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
