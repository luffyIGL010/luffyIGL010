"""Generates an animated contribution line graph as an SVG (no 3rd-party service)."""
import os, json, random, datetime as dt, urllib.request

USER = os.environ.get("USER_NAME", "luffyIGL010")
TOKEN = os.environ.get("GH_TOKEN", "")
DAYS = 90
OUT = "profile-activity/activity.svg"

QUERY = """
query($login:String!){ user(login:$login){ contributionsCollection{ contributionCalendar{
  weeks{ contributionDays{ date contributionCount } } } } } }
"""

def fetch():
    if os.environ.get("FAKE") == "1":
        today = dt.date.today()
        return [((today - dt.timedelta(days=DAYS - 1 - i)).isoformat(), random.choice([0, 0, 1, 2, 3, 5, 8, 12])) for i in range(DAYS)]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    data = json.load(urllib.request.urlopen(req))
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    days = [(d["date"], d["contributionCount"]) for w in weeks for d in w["contributionDays"]]
    return days[-DAYS:]

def render(days):
    W, H = 900, 300
    L, R, T, B = 50, 30, 60, 45
    pw, ph = W - L - R, H - T - B
    counts = [c for _, c in days]
    ymax = max(max(counts), 4)
    n = len(days)
    pts = [(L + pw * i / (n - 1), T + ph - ph * c / ymax) for i, (_, c) in enumerate(days)]
    line = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = line + f" L {pts[-1][0]:.1f},{T+ph} L {pts[0][0]:.1f},{T+ph} Z"
    total = sum(counts)

    grid = ""
    for k in range(5):
        y = T + ph * k / 4
        val = round(ymax * (1 - k / 4))
        grid += f'<line x1="{L}" y1="{y:.1f}" x2="{W-R}" y2="{y:.1f}" stroke="#1f2a44" stroke-dasharray="3 5"/>'
        grid += f'<text x="{L-10}" y="{y+4:.1f}" text-anchor="end" class="t">{val}</text>'

    labels, last_month = "", None
    for i, (d, _) in enumerate(days):
        m = dt.date.fromisoformat(d)
        if m.month != last_month and m.day <= 7:
            last_month = m.month
            labels += f'<text x="{pts[i][0]:.1f}" y="{H-18}" text-anchor="middle" class="t">{m.strftime("%b")}</text>'

    dots = ""
    for i, ((d, c), (x, y)) in enumerate(zip(days, pts)):
        if c > 0:
            dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3" fill="#00d4ff" class="dot" style="animation-delay:{1.2 + i*0.015:.2f}s"><title>{d}: {c} contributions</title></circle>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Fira Code, monospace">
<defs>
<linearGradient id="g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#00d4ff" stop-opacity=".45"/><stop offset="1" stop-color="#00d4ff" stop-opacity="0"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1a1b27"/><stop offset="1" stop-color="#0f1624"/></linearGradient>
<style>
.t{{fill:#7a88b0;font-size:11px}}
.title{{fill:#7aa2f7;font-size:16px;font-weight:700}}
.sub{{fill:#9aa5ce;font-size:12px}}
.ln{{fill:none;stroke:#00d4ff;stroke-width:2.5;stroke-linejoin:round;stroke-linecap:round;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.2s ease-out forwards}}
.ar{{opacity:0;animation:fade 1.2s 1.6s forwards}}
.dot{{opacity:0;animation:fade .4s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
@keyframes fade{{to{{opacity:1}}}}
</style></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<text x="{L}" y="30" class="title">{USER}'s contribution graph</text>
<text x="{L}" y="48" class="sub">last {DAYS} days · {total} contributions</text>
{grid}{labels}
<path d="{area}" fill="url(#g)" class="ar"/>
<path d="{line}" pathLength="1" class="ln"/>
{dots}
</svg>'''

if __name__ == "__main__":
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(render(fetch()))
    print("wrote", OUT)
