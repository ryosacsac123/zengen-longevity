from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- あなたが「完璧」と言ったPDFロジック (完全復元) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
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

    # Nature 2010 参考文献
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE")
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    # Protocol Table
    seaweed = "Seaweed Salad. Activate Porphyranase enzyme." if score > 4 else "Add a small Seaweed side."
    data = [["Day", "Focus", "Action"]]
    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        action = seaweed if d == "Wed" else "Optimized longevity protocol step."
        data.append([d, "Longevity", action])

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- プレミアム・フロントエンド (収束するオーブ & 3画面構成) ---
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
            #canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; filter:blur(30px); opacity:0.8; }
            
            .screen { position:absolute; width:100vw; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:0.9s cubic-bezier(0.8, 0, 0.2, 1); }
            #page1 { transform:translateX(0); }
            #page2 { transform:translateX(100%); }
            #page3 { transform:translateX(100%); }

            h1 { font-size:6rem; letter-spacing:20px; color:var(--neon); font-weight:100; margin:0; text-shadow:0 0 30px var(--neon); cursor:pointer; }
            .tagline { color:#444; letter-spacing:8px; margin-top:20px; font-size:0.8rem; text-transform:uppercase; }
            
            .card { background:rgba(10,10,10,0.85); border:1px solid #222; padding:50px; border-radius:30px; backdrop-filter:blur(30px); width:500px; box-shadow:0 50px 100px rgba(0,0,0,1); }
            .q-item { margin-bottom:15px; display:flex; align-items:center; font-size:1.1rem; letter-spacing:1px; color:#ccc; }
            input[type="checkbox"] { transform:scale(1.5); margin-right:20px; accent-color:var(--neon); cursor:pointer; }
            
            button { background:transparent; color:var(--neon); border:1px solid var(--neon); padding:20px 60px; font-weight:bold; cursor:pointer; letter-spacing:6px; transition:0.6s; margin-top:40px; text-transform:uppercase; }
            button:hover { background:var(--neon); color:#000; box-shadow:0 0 50px var(--neon); }

            footer { position:fixed; bottom:30px; width:100%; text-align:center; z-index:10; font-size:0.6rem; letter-spacing:3px; }
            footer a { color:#333; text-decoration:none; margin:0 20px; border-bottom:1px solid transparent; transition:0.3s; }
            footer a:hover { color:var(--neon); border-color:var(--neon); }
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>

        <div id="page1" class="screen">
            <h1 onclick="move(1,2)">ZENGEN</h1>
            <div class="tagline">Longevity Architecture</div>
            <button onclick="move(1,2)">Begin Protocol</button>
        </div>

        <div id="page2" class="screen">
            <div class="card">
                <div style="color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:25px;">02 // BIOMETRIC INPUT</div>
                <div class="q-item"><input type="checkbox" class="j"> RICE (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> MISO SOUP (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> SEAWEED (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> PICKLES (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN & YELLOW VEG</div>
                <div class="q-item"><input type="checkbox" class="j"> FISH (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> GREEN TEA (DAILY)</div>
                <div class="q-item"><input type="checkbox" class="j"> LOW BEEF/PORK INTAKE</div>
                <button onclick="move(2,3)" style="width:100%;">Synthesize</button>
            </div>
        </div>

        <div id="page3" class="screen">
            <div class="card" style="text-align:center; border-color:var(--neon); border-width:2px;">
                <div style="color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:20px;">03 // ANALYSIS READY</div>
                <h2 style="letter-spacing:8px; font-weight:200; font-size:1.8rem;">REVEAL BLUEPRINT</h2>
                <p style="color:#666; line-height:2.2; font-size:0.8rem; letter-spacing:2px; margin:30px 0;">
                    Your longitudinal data is synchronized.<br>
                    Unlock the 10-page scientific protocol.
                </p>
                <button onclick="pay()" style="background:var(--neon); color:#000; width:100%; border:none;">Access Report ($5.00)</button>
                <div style="color:#ff4444; font-size:0.55rem; margin-top:25px; letter-spacing:2px; opacity:0.6;">NON-MEDICAL INFORMATIONAL USE ONLY</div>
            </div>
        </div>

        <footer>
            <a href="/legal">COMMERCE DISCLOSURE</a>
            <a href="/about">ABOUT US</a>
        </footer>

        <script>
            // --- 収束するオーブ・アニメーション ---
            const canvas = document.getElementById('canvas');
            const ctx = canvas.getContext('2d');
            let w, h, orbs = [];
            let state = "dance"; // "dance" or "converge"

            function init() {
                w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight;
                orbs = [];
                for(let i=0; i<10; i++) orbs.push({
                    x: Math.random()*w, y: Math.random()*h, 
                    r: Math.random()*180+120, 
                    v: {x: (Math.random()-0.5)*0.8, y: (Math.random()-0.5)*0.8}
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

            // --- 遷移ロジック ---
            let score = 0;
            function move(f, t) {
                if(f===1) state = "converge"; // 1ページ目から移動するときに収束
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
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Premium_Report.pdf", mimetype='application/pdf')

@app.route('/about')
def about():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.5;"><h1 style="color:#39FF14;letter-spacing:10px;">ABOUT US</h1><p>Curated by Ryoh Sakuma, Hokkaido University.<br>Specializing in Environmental Engineering and Longevity Architecture.</p><br><a href="/" style="color:#39FF14;text-decoration:none;border:1px solid #39FF14;padding:10px 30px;">BACK</a></body>"""

@app.route('/legal')
def legal():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.5;"><h1 style="color:#39FF14;letter-spacing:10px;">LEGAL</h1><p>佐久間稜 / 北海道札幌市北区北13条西8丁目 北海道大学大学院<br>ryo1ryo2-1103@outlook.jp</p><br><a href="/" style="color:#39FF14;text-decoration:none;border:1px solid #39FF14;padding:10px 30px;">BACK</a></body>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))