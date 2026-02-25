from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- 1. あなたが「完璧」と言った2ページ構成のPDFエンジン (完全復元) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- PAGE 1: デザイン & 診断結果 ---
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT") [cite: 7]
    
    # スコア円
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8") [cite: 8]
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 240, "JDI8 SCORE") [cite: 9]
    
    risk = "HIGH" if score <= 4 else "MODERATE"
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, f"RISK ASSESSMENT: {risk}") [cite: 10]

    # Section 02: THE JAPANESE GENETIC EDGE
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE") [cite: 11]
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.") [cite: 12]

    # Section 03: PERSONALIZED PROTOCOL
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL") [cite: 13]

    # 完璧なテーブルデータの復元
    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", "Seaweed side dish. Support marine polysaccharide digestion."],
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
        ] [cite: 14]

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)

    p.showPage() # --- PAGE 2: THE GOLD STANDARD STACK ---
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "04 // THE GOLD STANDARD STACK") [cite: 15]

    items = [
        ("Ippodo Matcha", "Finest L-Theanine source.", "https://amzn.to/3ZgMv0Q"),
        ("NMN", "NAD+ precursor for DNA repair and cellular energy.", "https://amzn.to/4qTcOHM"),
        ("Spermidine", "Autophagy inducer.", "https://amzn.to/4tYE6j2"),
        ("EPA/DHA", "Inflammation control.", "https://amzn.to/4kRTklz"),
        ("Zojirushi IH", "Metabolism foundation.", "https://amzn.to/4hfC1sA")
    ] [cite: 16-30]

    y = height - 80
    for title, desc, link in items:
        p.setFont("Helvetica-Bold", 11)
        p.setFillColor(colors.white)
        p.drawString(40, y, f"> {title}:")
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.lightgrey)
        p.drawString(50, y - 15, desc)
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(50, y - 30, f"View on Amazon: {link}")
        y -= 60

    p.save()
    buffer.seek(0)
    return buffer

# --- 2. プレミアム3画面UI (中央収束アニメーション & 英文免責) ---
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Longevity</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { margin:0; overflow:hidden; background:var(--bg); color:#fff; font-family:'Helvetica Neue', sans-serif; }
            #canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; filter:blur(40px); opacity:0.8; }
            
            .screen { position:absolute; width:100vw; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:0.9s cubic-bezier(0.8, 0, 0.2, 1); }
            #page1 { transform:translateX(0); }
            #page2 { transform:translateX(100%); }
            #page3 { transform:translateX(100%); }

            h1 { font-size:6rem; letter-spacing:25px; color:var(--neon); font-weight:100; margin:0; text-shadow:0 0 30px var(--neon); cursor:pointer; }
            .tagline { color:#444; letter-spacing:10px; margin-top:20px; font-size:0.8rem; text-transform:uppercase; }
            
            .card { background:rgba(10,10,10,0.85); border:1px solid #222; padding:50px; border-radius:35px; backdrop-filter:blur(30px); width:520px; box-shadow:0 60px 120px rgba(0,0,0,1); }
            .q-item { margin-bottom:15px; display:flex; align-items:center; font-size:1.1rem; letter-spacing:1px; color:#ccc; }
            input[type="checkbox"] { transform:scale(1.5); margin-right:20px; accent-color:var(--neon); cursor:pointer; }
            
            button { background:transparent; color:var(--neon); border:1px solid var(--neon); padding:20px 65px; font-weight:bold; cursor:pointer; letter-spacing:6px; transition:0.6s; margin-top:40px; text-transform:uppercase; }
            button:hover { background:var(--neon); color:#000; box-shadow:0 0 50px var(--neon); }

            .disclaimer { font-size:0.7rem; color:#555; line-height:1.6; border-top:1px solid #222; margin-top:30px; padding-top:20px; text-align:justify; }
            footer { position:fixed; bottom:30px; width:100%; text-align:center; z-index:10; font-size:0.6rem; letter-spacing:3px; }
            footer a { color:#333; text-decoration:none; margin:0 20px; transition:0.3s; }
            footer a:hover { color:var(--neon); }
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>

        <div id="page1" class="screen">
            <h1 onclick="move(1,2)">ZENGEN</h1>
            <div class="tagline">Biological Architecture</div>
            <button onclick="move(1,2)">Initiate Analysis</button>
        </div>

        <div id="page2" class="screen">
            <div class="card">
                <div style="color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:20px;">02 // BIOMETRIC INPUT</div>
                <div class="q-item"><input type="checkbox" class="j"> RICE (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> MISO SOUP (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> SEAWEED (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> PICKLES (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN & YELLOW VEG</div>
                <div class="q-item"><input type="checkbox" class="j"> FISH (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN TEA (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> LOW MEAT INTAKE</div>
                <button onclick="move(2,3)" style="width:100%;">Synthesize</button>
                
                <div class="disclaimer">
                    <strong>ABOUT US:</strong> Developed by Ryoh Sakuma, Hokkaido University Graduate School of Engineering. Rooted in environmental engineering and biological data architecture.<br><br>
                    <strong>DISCLAIMER:</strong> This service is a biological data engine for informational purposes only. It is not a medical diagnostic tool and does not provide medical efficacy or professional advice. Always consult a physician for health-related decisions.
                </div>
            </div>
        </div>

        <div id="page3" class="screen">
            <div class="card" style="text-align:center; border-color:var(--neon);">
                <div style="color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:20px;">03 // ANALYSIS READY</div>
                <h2 style="letter-spacing:10px; font-weight:100; font-size:2rem; margin:0;">UNLOCK BLUEPRINT</h2>
                <p style="color:#666; line-height:2.4; font-size:0.85rem; letter-spacing:2px; margin:35px 0;">
                    Your longitudinal data is synchronized.<br>Unlock the premium 10-page scientific protocol.
                </p>
                <button onclick="toPayment()" style="background:var(--neon); color:#000; width:100%; border:none;">Access Report ($5.00)</button>
            </div>
        </div>

        <footer>
            <a href="/legal">LEGAL</a>
            <a href="/about">ABOUT US</a>
        </footer>

        <script>
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            let w, h, orbs = [];
            let state = "dance"; 

            function init() {
                w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight;
                orbs = [];
                for(let i=0; i<15; i++) orbs.push({
                    x: Math.random()*w, y: Math.random()*h, 
                    r: Math.random()*180+120, 
                    v: {x: (Math.random()-0.5)*0.5, y: (Math.random()-0.5)*0.5}
                });
            }

            function draw() {
                ctx.clearRect(0,0,w,h);
                orbs.forEach(o => {
                    if(state === "dance") {
                        o.x += o.v.x; o.y += o.v.y;
                        if(o.x<0||o.x>w) o.v.x*=-1; if(o.y<0||o.y>h) o.v.y*=-1;
                    } else {
                        // 中央へ収束
                        o.x += (w/2 - o.x) * 0.02;
                        o.y += (h/2 - o.y) * 0.02;
                    }
                    let g = ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r);
                    g.addColorStop(0, 'rgba(57, 255, 20, 0.4)'); g.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
                });
                requestAnimationFrame(draw);
            }
            window.onresize=init; init(); draw();

            let score = 0;
            function move(f, t) {
                if(f===1) state = "converge"; 
                score = document.querySelectorAll('.j:checked').length;
                document.getElementById('page'+f).style.transform = 'translateX(-100%)';
                document.getElementById('page'+t).style.transform = 'translateX(0)';
            }
            function toPayment() {
                // ここで本来のStripe決済画面へ飛ばす。今はまだ決済を挟まずPDFへ進む場合は修正が必要
                window.location.href=`/download-report?score=${score}`;
            }
        </script>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Report.pdf", mimetype='application/pdf')

@app.route('/about')
def about():
    return "Curated by Ryoh Sakuma, Hokkaido University. (Full About Us content here)"

@app.route('/legal')
def legal():
    return "Commerce Disclosure (佐久間稜 / 北海道大学...)"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)