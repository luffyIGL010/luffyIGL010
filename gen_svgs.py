import html

THEMES = {
  "dark":  dict(bg1="#0d1117", bg2="#161b22", card="#1c2230", border="#30363d", text="#e6edf3", muted="#8b949e", accent="#58a6ff", accent2="#bc8cff", green="#3fb950"),
  "light": dict(bg1="#ffffff", bg2="#f6f8fa", card="#ffffff", border="#d0d7de", text="#1f2328", muted="#57606a", accent="#0969da", accent2="#8250df", green="#1a7f37"),
}
FONT = "Segoe UI, -apple-system, Helvetica, Arial, sans-serif"
e = html.escape

def head(w, h, t, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" font-family="{FONT}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{t['bg1']}"/><stop offset="1" stop-color="{t['bg2']}"/></linearGradient>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{t['accent']}"/><stop offset="1" stop-color="{t['accent2']}"/></linearGradient>
<style>
.fade{{opacity:0;animation:fade .8s ease-out forwards}}
.slide{{opacity:0;transform:translateY(14px);animation:slide .8s ease-out forwards}}
@keyframes fade{{to{{opacity:1}}}}
@keyframes slide{{to{{opacity:1;transform:translateY(0)}}}}
@keyframes pulse{{0%,100%{{opacity:1}}50%{{opacity:.25}}}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
{extra_css}
</style></defs>
<rect width="{w}" height="{h}" rx="16" fill="url(#bg)" stroke="{t['border']}"/>'''

def hero(t):
    chips = ["Computer Vision", "NLP", "GenAI", "AI Agents"]
    x, chip_svg = 60, ""
    for i, c in enumerate(chips):
        cw = int(len(c) * 8.2 + 28)
        chip_svg += (f'<g class="slide" style="animation-delay:{0.9+i*0.15:.2f}s"><rect x="{x}" y="196" width="{cw}" height="30" rx="15" fill="none" stroke="{t["accent"]}" stroke-opacity=".55"/>'
                     f'<text x="{x+cw/2}" y="216" text-anchor="middle" font-size="13" fill="{t["accent"]}">{e(c)}</text></g>')
        x += cw + 12
    return head(900, 260, t, ".orb{animation:float 6s ease-in-out infinite}.dot{animation:pulse 1.6s infinite}") + f'''
<g opacity=".5"><circle class="orb" cx="790" cy="150" r="90" fill="none" stroke="url(#ac)" stroke-width="2"/>
<circle class="orb" cx="790" cy="150" r="55" fill="none" stroke="url(#ac)" stroke-width="2" style="animation-delay:-2s"/>
<circle class="orb" cx="790" cy="150" r="20" fill="url(#ac)" style="animation-delay:-4s"/></g>
<g class="fade" style="animation-delay:.1s"><circle class="dot" cx="64" cy="52" r="5" fill="{t['green']}"/>
<text x="78" y="57" font-size="14" fill="{t['green']}" font-weight="600">Open to work</text></g>
<text class="slide" style="animation-delay:.2s" x="60" y="122" font-size="56" font-weight="800" fill="url(#ac)">Saurav Rauthan</text>
<text class="slide" style="animation-delay:.45s" x="60" y="158" font-size="22" font-weight="600" fill="{t['text']}">AI / ML Engineer  ·  Python AI Developer</text>
<text class="slide" style="animation-delay:.65s" x="60" y="184" font-size="15" fill="{t['muted']}">Building AI products that actually ship</text>
{chip_svg}
</svg>'''

def about(t):
    rows = [
        "Building AI products end to end, from model to deployed app",
        "Currently working on GenAI apps, AI agents and DSA",
        "Based in Dehradun, Uttarakhand  ·  Open to AI Developer / ML Engineer roles",
        "sauravrauthan82@gmail.com",
    ]
    body = ""
    for i, r in enumerate(rows):
        y = 112 + i * 38
        body += (f'<g class="slide" style="animation-delay:{0.2+i*0.18:.2f}s"><circle cx="64" cy="{y-5}" r="4" fill="url(#ac)"/>'
                 f'<text x="84" y="{y}" font-size="17" fill="{t["text"]}">{e(r)}</text></g>')
    return head(900, 250, t) + f'''
<rect x="40" y="36" width="5" height="28" rx="2.5" fill="url(#ac)"/>
<text x="58" y="58" font-size="26" font-weight="800" fill="{t['text']}">About</text>
{body}
</svg>'''

def creds(t):
    cards = [
        ("EDUCATION", "B.Tech, AI &amp; ML", ["Dr. APJ Abdul Kalam Institute", "of Technology, Champawat", "Class of 2026"]),
        ("EXPERIENCE", "Data Science Intern", ["CodSoft", "Hands-on machine learning", "tasks on real datasets"]),
        ("ACHIEVEMENT", "2nd Place", ["UCOST state-level", "science competition", "Uttarakhand"]),
    ]
    body = ""
    for i, (lab, title, lines) in enumerate(cards):
        x = 40 + i * 280
        ls = "".join(f'<text x="{x+22}" y="{176+j*22}" font-size="14" fill="{t["muted"]}">{l}</text>' for j, l in enumerate(lines))
        body += (f'<g class="slide" style="animation-delay:{0.2+i*0.25:.2f}s">'
                 f'<rect x="{x}" y="92" width="260" height="150" rx="12" fill="{t["card"]}" stroke="{t["border"]}"/>'
                 f'<rect x="{x}" y="92" width="260" height="4" rx="2" fill="url(#ac)"/>'
                 f'<text x="{x+22}" y="124" font-size="12" font-weight="700" letter-spacing="1.5" fill="{t["accent"]}">{lab}</text>'
                 f'<text x="{x+22}" y="152" font-size="19" font-weight="700" fill="{t["text"]}">{title}</text>{ls}</g>')
    return head(900, 270, t) + f'''
<rect x="40" y="36" width="5" height="28" rx="2.5" fill="url(#ac)"/>
<text x="58" y="58" font-size="26" font-weight="800" fill="{t['text']}">Credentials</text>
{body}
</svg>'''

for name, t in THEMES.items():
    open(f"{'' if name=='dark' else ''}{name}.svg", "w", encoding="utf-8").write(hero(t))
    open(f"about-{name}.svg", "w", encoding="utf-8").write(about(t))
    open(f"credentials-{name}.svg", "w", encoding="utf-8").write(creds(t))
print("ok")
