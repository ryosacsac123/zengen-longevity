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

# --- PDF Generation (あなたの「完璧なデザイン」) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    # 1ページ目
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
    for day in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
        action = seaweed if day == "Wed" else "Optimized longevity protocol step."
        data.append([day, "Longevity", action])

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

# --- Routes ---

@app.route('/')
def home():
    # 3画面（スライド）構成のUI
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN Longevity</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { background: var(--bg); color: #fff; font-family: 'Helvetica', sans-serif; margin:0; overflow:hidden; }
            .screen { width: 100vw; height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; transition: 0.8s cubic-bezier(0.4, 0, 0.2, 1); position: absolute; }
            
            /* 初期位置の設定 */
            #page1 { transform: translateX(0); }
            #page2 { transform: translateX(100%); }
            #page3 { transform: translateX(100%); }

            h1 { font-size: 4rem; letter-spacing: 10px; color: var(--neon); }
            .card { background: #111; border: 1px solid #333; padding: 40px; border-radius: 20px; width: 400px; text-align: left; }
            .q { margin-bottom: 10px; display: flex; align-items: center; font-size: 1.1rem; }
            input[type="checkbox"] { transform: scale(1.5); margin-right: 15px; accent-color: var(--neon); }
            
            button { background: var(--neon); color: #000; border: none; padding: 20px 40px; font-weight: bold; cursor: pointer; border-radius: 5px; font-size: 1.1rem; transition: 0.3s; margin-top: 20px; width: 100%; }
            button:hover { background: #fff; transform: scale(1.05); }
            
            .preview-list { color: #888; text-align: left; line-height: 1.8; margin-bottom: 20px; }
            .neon-text { color: var(--neon); }
            footer { position: fixed; bottom: 20px; width: 100%; text-align: center; font-size: 0.7rem; }
            footer a { color: #333; text-decoration: none; }
        </style>
    </head>
    <body>

        <div id="page1" class="screen">
            <h1>ZENGEN</h1>
            <p style="font-style: italic; color: #555;">Longevity Blueprint Architecture</p>
            <button onclick="toPage2()" style="width: auto;">START DIAGNOSIS</button>
        </div>

        <div id="page2" class="screen">
            <div class="card">
                <h2 style="color:var(--neon); margin-top:0;">BIOLOGICAL INPUT</h2>
                <div class="q"><input type="checkbox" class="j"> Rice (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Miso Soup (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Seaweed (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Pickles (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Green & Yellow Veg (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Fish (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Green Tea (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Low Meat Intake</div>
                <button onclick="toPage3()">CALCULATE SCORE</button>
            </div>
        </div>

        <div id="page3" class="screen">
            <div class="card" style="text-align: center;">
                <h2 style="color:var(--neon);">PREMIUM ACCESS</h2>
                <div class="preview-list">
                    ● <span class="neon-text">JDI8</span> Science-backed Score<br>
                    ● <span class="neon-text">7-Day</span> Personalized Protocol<br>
                    ● <span class="neon-text">Marine</span> Enzyme Pathway Analysis<br>
                    ● <span class="neon-text">Longevity</span> Stack Recommendations
                </div>
                <p>Unlock your 10-page biological blueprint.</p>
                <button onclick="getPDF()">GET PREMIUM PDF ($5)</button>
                <p style="font-size: 0.8rem; color: #444; margin-top: 15px;">※決済完了後、PDFが即時発行されます</p>
            </div>
        </div>

        <footer><a href="/legal">Commerce Disclosure</a></footer>

        <script>
            let score = 0;
            function toPage2() {
                document.getElementById('page1').style.transform = 'translateX(-100%)';
                document.getElementById('page2').style.transform = 'translateX(0)';
            }
            function toPage3() {
                score = document.querySelectorAll('.j:checked').length;
                document.getElementById('page2').style.transform = 'translateX(-100%)';
                document.getElementById('page3').style.transform = 'translateX(0)';
            }
            function getPDF() {
                // 本番はここでStripe決済。一旦PDF取得リンクへ
                window.location.href = `/download-report?score=${score}`;
            }
        </script>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Report_{score}.pdf", mimetype='application/pdf')

@app.route('/legal')
def legal():
    return """
    <body style="background:#000; color:#fff; font-family:sans-serif; padding:40px;">
        <h1 style="color:#39FF14;">特定商取引法に基づく表記</h1>
        <p><b>販売業者:</b> 佐久間稜</p>
        <p><b>所在地:</b> 〒060-0813 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院</p>
        <p><b>価格:</b> $5.00</p>
        <a href="/" style="color:#39FF14;">戻る</a>
    </body>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))