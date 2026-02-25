from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- 1. あなたの「完璧な」PDFロジック (完全復元) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    # 1ページ目：漆黒の背景とネオングリーン
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.circle(width/2, height - 150, 70, stroke=1)
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    risk = "LOW" if score >= 7 else "MODERATE" if score >= 4 else "HIGH"
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(width/2, height - 270, f"RISK ASSESSMENT: {risk}")

    # Protocol Table
    seaweed = "Seaweed side dish. Support marine polysaccharide digestion."
    data = [["Day", "Focus", "Action"]]
    for d in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        action = seaweed if d == "Wed" else "Optimized longevity protocol step."
        data.append([d, "Longevity", action])

    table = Table(data, colWidths=[50, 80, 380])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
    ]))
    table.wrapOn(p, 40, 420)
    table.drawOn(p, 40, height - 600)
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- 2. プレミアム3画面UI (JavaScriptオーブ・スライドアニメーション) ---

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Architecture</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { margin: 0; overflow: hidden; background: var(--bg); font-family: 'Helvetica Neue', sans-serif; color: #fff; }
            #bg-canvas { position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: -1; filter: blur(40px); opacity: 0.6; }

            .container { position: relative; width: 100vw; height: 100vh; }
            .screen { position: absolute; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: transform 0.8s cubic-bezier(0.86, 0, 0.07, 1); }
            
            #page1 { transform: translateX(0); }
            #page2 { transform: translateX(100%); }
            #page3 { transform: translateX(100%); }

            h1 { font-size: 5rem; letter-spacing: 15px; color: var(--neon); font-weight: 200; text-shadow: 0 0 30px var(--neon); }
            .card { background: rgba(15, 15, 15, 0.7); border: 1px solid #222; padding: 50px; border-radius: 30px; backdrop-filter: blur(15px); width: 450px; text-align: left; }
            
            .q-item { margin-bottom: 12px; display: flex; align-items: center; font-size: 1.1rem; letter-spacing: 1px; }
            input[type="checkbox"] { transform: scale(1.4); margin-right: 20px; accent-color: var(--neon); }
            
            button { background: transparent; color: var(--neon); border: 1px solid var(--neon); padding: 18px 50px; font-weight: bold; cursor: pointer; border-radius: 4px; transition: 0.4s; letter-spacing: 3px; }
            button:hover { background: var(--neon); color: #000; box-shadow: 0 0 30px var(--neon); }
            
            .val-list { color: #888; line-height: 2; margin: 20px 0; }
            footer { position: fixed; bottom: 20px; width: 100%; text-align: center; }
            footer a { color: #333; text-decoration: none; font-size: 0.7rem; letter-spacing: 2px; }
        </style>
    </head>
    <body>
        <canvas id="bg-canvas"></canvas>

        <div id="page1" class="screen">
            <h1>ZENGEN</h1>
            <p style="color:#555; letter-spacing:5px;">Longevity Architecture</p>
            <button onclick="move(1, 2)">ACCESS DIAGNOSIS</button>
        </div>

        <div id="page2" class="screen">
            <div class="card">
                <h2 style="color:var(--neon); letter-spacing:3px;">BIOMETRIC INPUT</h2>
                <div class="q-item"><input type="checkbox" class="j"> Rice (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Miso Soup (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Seaweed (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Pickles (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Green & Yellow Veg</div>
                <div class="q-item"><input type="checkbox" class="j"> Fish (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Green Tea (Daily)</div>
                <div class="q-item"><input type="checkbox" class="j"> Low Meat Intake</div>
                <button onclick="move(2, 3)" style="width:100%;">GENERATE SCORE</button>
            </div>
        </div>

        <div id="page3" class="screen">
            <div class="card" style="text-align:center;">
                <h2 style="color:var(--neon);">PREMIUM BLUEPRINT</h2>
                <div class="val-list">
                    ● ARCHITECTURAL LONGEVITY SCORE<br>
                    ● 7-DAY PERSONALIZED PROTOCOL<br>
                    ● GOLD STANDARD STACK LIST
                </div>
                <button onclick="pay()" style="background:var(--neon); color:#000; width:100%;">DOWNLOAD REPORT ($5)</button>
            </div>
        </div>

        <footer><a href="/legal">COMMERCE DISCLOSURE</a></footer>

        <script>
            // --- ORB ANIMATION ---
            const canvas = document.getElementById('bg-canvas');
            const ctx = canvas.getContext('2d');
            let w, h;
            const orbs = [];
            function init() {
                w = canvas.width = window.innerWidth;
                h = canvas.height = window.innerHeight;
                for(let i=0; i<6; i++) orbs.push({x:Math.random()*w, y:Math.random()*h, r:Math.random()*150+100, dx:(Math.random()-0.5)*0.3, dy:(Math.random()-0.5)*0.3});
            }
            function draw() {
                ctx.clearRect(0,0,w,h);
                orbs.forEach(o => {
                    o.x += o.dx; o.y += o.dy;
                    if(o.x<0 || o.x>w) o.dx*=-1; if(o.y<0 || o.y>h) o.dy*=-1;
                    let g = ctx.createRadialGradient(o.x, o.y, 0, o.x, o.y, o.r);
                    g.addColorStop(0, 'rgba(57, 255, 20, 0.3)'); g.addColorStop(1, 'rgba(0,0,0,0)');
                    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
                });
                requestAnimationFrame(draw);
            }
            window.onresize = init; init(); draw();

            // --- NAVIGATION ---
            let score = 0;
            function move(from, to) {
                score = document.querySelectorAll('.j:checked').length;
                document.getElementById('page'+from).style.transform = 'translateX(-100%)';
                document.getElementById('page'+to).style.transform = 'translateX(0)';
            }
            function pay() { window.location.href = `/download-report?score=${score}`; }
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
    return """<body style="background:#000;color:#fff;padding:50px;font-family:sans-serif;"><h1 style="color:#39FF14;">特定商取引法に基づく表記</h1><p>販売業者: 佐久間稜<br>所在地: 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院<br>電話番号: 090-6446-6654<br>販売価格: $5.00</p><a href="/" style="color:#39FF14;">戻る</a></body>"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))