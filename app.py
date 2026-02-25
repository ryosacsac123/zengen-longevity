from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- Amazon Affiliate Links ---
LINKS = {
    "Ippodo Matcha": "https://amzn.to/3ZgMv0Q",
    "NMN": "https://amzn.to/4qTcOHM",
    "Spermidine": "https://amzn.to/4tYE6j2",
    "EPA/DHA": "https://amzn.to/4kRTklz",
    "Zojirushi IH": "https://amzn.to/4hfC1sA"
}

# --- 1. あなたが「完璧」と言ったPDFエンジン (完全復元) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Page 1: Design
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 240, "JDI8 SCORE")
    
    risk_text = "RISK ASSESSMENT: HIGH" if score <= 4 else "RISK ASSESSMENT: MODERATE"
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, risk_text)

    # Section 02: Genetic Edge
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE")
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    # Section 03: Protocol
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", "Add a small Seaweed side to your lunch."],
            ["Thu", "Recovery", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Omega-3: Take 1g EPA/DHA supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "Focus on 20min hot soak to activate HSP."]
        ]
    else:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "16:8 Fasting. Break fast with Miso & Seaweed."],
            ["Tue", "Microbiome", "Microbiome Diversity: Mix Natto with Okra/Kimchi."],
            ["Wed", "Enzyme", "Seaweed Salad. Activate Porphyranase enzyme."],
            ["Thu", "Nootropic", "2g Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "Fatty fish (Salmon/Saba) + 1g supplement."],
            ["Sat", "Metabolism", "HIIT Session. Activate glycolysis."],
            ["Sun", "Rest", "Hot Bath + 5min cold shower for recovery."]
        ]

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)

    p.showPage() # Page 2: Stocks
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "04 // THE GOLD STANDARD STACK")

    y_pos = height - 80
    items = [
        ("Ippodo Matcha", "Finest L-Theanine source.", LINKS["Ippodo Matcha"]),
        ("NMN", "NAD+ precursor for DNA repair.", LINKS["NMN"]),
        ("Spermidine", "Autophagy inducer.", LINKS["Spermidine"]),
        ("EPA/DHA", "Inflammation control.", LINKS["EPA/DHA"]),
        ("Zojirushi IH", "Metabolism foundation.", LINKS["Zojirushi IH"])
    ]
    for title, desc, link in items:
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(colors.white)
        p.drawString(40, y_pos, f"> {title}:")
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.lightgrey)
        p.drawString(50, y_pos - 15, desc)
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(50, y_pos - 30, f"View on Amazon: {link}")
        y_pos -= 60

    p.save()
    buffer.seek(0)
    return buffer

# --- 2. プレミアム3画面UI (オーブ、About Us、決済) ---

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Longevity Architecture</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { margin:0; overflow:hidden; background:var(--bg); color:#fff; font-family:'Helvetica Neue', sans-serif; }
            #bg-canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; filter:blur(40px); opacity:0.6; }
            
            .container { position:relative; width:100vw; height:100vh; }
            .screen { position:absolute; width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:transform 0.8s cubic-bezier(0.85, 0, 0.15, 1); }
            
            #page1 { transform:translateX(0); }
            #page2 { transform:translateX(100%); }
            #page3 { transform:translateX(100%); }

            h1 { font-size:5rem; letter-spacing:15px; color:var(--neon); font-weight:100; margin:0; text-shadow:0 0 20px var(--neon); }
            .about-us { color:#666; font-size:0.8rem; max-width:400px; text-align:center; line-height:1.8; margin-top:30px; letter-spacing:1px; }
            
            .card { background:rgba(10,10,10,0.8); border:1px solid #222; padding:45px; border-radius:30px; backdrop-filter:blur(20px); width:480px; text-align:left; box-shadow:0 30px 60px rgba(0,0,0,0.8); }
            .q-item { margin-bottom:12px; display:flex; align-items:center; font-size:1rem; letter-spacing:1px; }
            input[type="checkbox"] { transform:scale(1.4); margin-right:20px; accent-color:var(--neon); cursor:pointer; }
            
            button { background:transparent; color:var(--neon); border:1px solid var(--neon); padding:18px 50px; font-weight:bold; cursor:pointer; letter-spacing:4px; transition:0.4s; margin-top:30px; text-transform:uppercase; }
            button:hover { background:var(--neon); color:#000; box-shadow:0 0 30px var(--neon); }
            
            .ref { margin-top:30px; border-top:1px solid #222; padding-top:20px; font-size:0.7rem; color:#555; letter-spacing:1px; }
            footer { position:fixed; bottom:20px; width:100%; text-align:center; z-index:10; font-size:0.6rem; letter-spacing:2px; color:#333; }
            footer a { color:#333; text-decoration:none; margin:0 15px; }
        </style>
    </head>
    <body>
        <canvas id="bg-canvas"></canvas>

        <div id="page1" class="screen">
            <h1>ZENGEN</h1>
            <div class="about-us">
                Founded by Ryoh Sakuma, Hokkaido University Graduate School of Engineering.<br>
                Merging environmental science with biological longevity protocols.
            </div>
            <button onclick="move(1,2)">Access Analysis</button>
        </div>

        <div id="page2" class="screen">
            <div class="card">
                <h2 style="color:var(--neon); letter-spacing:4px; margin-top:0;">BIOMETRIC INPUT</h2>
                <div class="q-item"><input type="checkbox" class="j"> Rice (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Miso Soup (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Seaweed (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Pickles (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Green & Yellow Veg</div>
                <div class="q-item"><input type="checkbox" class="j"> Fish (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Green Tea (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Low Beef/Pork Intake</div>
                <button onclick="move(2,3)" style="width:100%;">Synthesize Data</button>
                <div class="ref">REF: Nature (2010): Porphyranase enzyme pathway identified.</div>
            </div>
        </div>

        <div id="page3" class="screen">
            <div class="card" style="text-align:center; border-color:var(--neon);">
                <h2 style="color:var(--neon); letter-spacing:4px;">BLUEPRINT READY</h2>
                <p style="color:#888; line-height:1.8; font-size:0.9rem;">
                    Unlock the 10-page scientific protocol containing your personalized JDI8 score, marine enzyme analysis, and longevity stack.
                </p>
                <div style="color:#ff4444; font-size:0.7rem; margin:20px 0; letter-spacing:1px; text-transform:uppercase;">
                    Caution: Non-medical informational report.
                </div>
                <button onclick="pay()" style="background:var(--neon); color:#000; width:100%; border:none;">Download Report ($5.00)</button>
            </div>
        </div>

        <footer>
            <a href="/legal">LEGAL</a>
            <a href="https://amzn.to/3ZgMv0Q">PARTNERS</a>
        </footer>

        <script>
            // --- Orb Animation ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let w, h, orbs = [];
            function init() {
                w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight;
                orbs = [];
                for(let i=0; i<6; i++) orbs.push({x:Math.random()*w, y:Math.random()*h, r:Math.random()*150+100, dx:(Math.random()-0.5)*0.4, dy:(Math.random()-0.5)*0.4});
            }
            function draw() {
                ctx.clearRect(0,0,w,h);
                orbs.forEach(o => {
                    o.x+=o.dx; o.y+=o.dy;
                    if(o.x<0||o.x>w) o.dx*=-1; if(o.y<0||o.y>h) o.dy*=-1;
                    let g = ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r);
                    g.addColorStop(0, 'rgba(57, 255, 20, 0.3)'); g.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
                });
                requestAnimationFrame(draw);
            }
            window.onresize=init; init(); draw();

            // --- Logic ---
            let score = 0;
            function move(f, t) {
                score = document.querySelectorAll('.j:checked').length;
                document.getElementById('page'+f).style.transform = 'translateX(-100%)';
                document.getElementById('page'+t).style.transform = 'translateX(0)';
            }
            function pay() { window.location.href=`/download-report?score=${score}`; }
        </script>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Report.pdf", mimetype='application/pdf')

@app.route('/legal')
def legal():
    return """<body style="background:#000;color:#fff;padding:60px;font-family:sans-serif;"><h1 style="color:#39FF14;">特定商取引法に基づく表記</h1><p>販売業者: 佐久間稜<br>所在地: 北海道大学大学院 工学院<br>価格: $5.00</p><a href="/" style="color:#39FF14;">戻る</a></body>"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)