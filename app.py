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

# --- 1. あなたが「完璧」と言ったPDFエンジン (完全維持) ---
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
    
    if score <= 3: risk_text = "RISK ASSESSMENT: HIGH"
    elif score <= 6: risk_text = "RISK ASSESSMENT: MODERATE"
    else: risk_text = "RISK ASSESSMENT: LOW"

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, risk_text)

    # Protocol Section
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    seaweed = "Seaweed side dish. Support marine polysaccharide digestion."
    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", seaweed],
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
            ["Wed", "Enzyme", "Seaweed Salad. Support marine polysaccharide digestion."],
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
    
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer

# --- 2. Routes (Stripe審査をパスしつつ、流動的なUIを提供) ---

@app.route('/')
def home():
    # プレミアム感を出すための、ミニマリズムなフロントエンド
    return """
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Longevity</title>
        <style>
            body { background:#000; color:#fff; font-family:'Helvetica', sans-serif; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; margin:0; overflow:hidden; }
            .content { text-align:center; animation: fadeIn 1.5s ease; }
            h1 { color:#39FF14; font-size:3.5rem; letter-spacing:8px; text-transform:uppercase; margin:0; }
            .tagline { color:#888; font-style:italic; margin-bottom:40px; }
            .card { background:rgba(20,20,20,0.8); border:1px solid #333; padding:40px; border-radius:20px; box-shadow:0 20px 50px rgba(0,0,0,0.9); }
            .q { display:flex; align-items:center; margin-bottom:15px; font-size:1.1rem; cursor:pointer; }
            input[type="checkbox"] { width:20px; height:20px; accent-color:#39FF14; margin-right:15px; }
            button { width:100%; background:#39FF14; color:#000; border:none; padding:20px; font-weight:bold; font-size:1rem; border-radius:8px; cursor:pointer; margin-top:20px; transition:0.3s; }
            button:hover { background:#fff; transform:scale(1.02); }
            footer { position:absolute; bottom:20px; font-size:0.7rem; }
            footer a { color:#333; text-decoration:none; transition:0.3s; }
            footer a:hover { color:#39FF14; }
            @keyframes fadeIn { from { opacity:0; transform:translateY(10px); } to { opacity:1; } }
        </style>
    </head>
    <body>
        <div class="content">
            <h1>ZENGEN AI</h1>
            <p class="tagline">Personalized Longevity Protocol Engine</p>
            <div class="card">
                <div class="q"><input type="checkbox" class="j"> Rice (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Miso Soup (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Seaweed (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Pickles (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Green & Yellow Veg (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Fish (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Green Tea (Daily)</div>
                <div class="q"><input type="checkbox" class="j"> Less Beef/Pork Intake</div>
                <button onclick="calc()">GET PREMIUM REPORT ($5)</button>
            </div>
        </div>
        <script>
            function calc() {
                let s = document.querySelectorAll('.j:checked').length;
                window.location.href = `/download-report?score=${s}`;
            }
        </script>
        <footer>
            <a href="/legal">COMMERCE DISCLOSURE (特定商取引法に基づく表記)</a>
        </footer>
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
    <html>
    <head><title>Legal | ZENGEN AI</title><meta name="robots" content="noindex"></head>
    <body style="background:#000; color:#fff; font-family:sans-serif; padding:60px; line-height:2.0;">
        <h1 style="color:#39FF14;">特定商取引法に基づく表記</h1>
        <p><b>販売業者:</b> 佐久間稜</p>
        <p><b>所在地:</b> 〒060-0813 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院</p>
        <p><b>電話番号:</b> 090-6446-6654</p>
        <p><b>メールアドレス:</b> ryo1ryo2-1103@outlook.jp</p>
        <p><b>販売価格:</b> $5.00</p>
        <p><b>支払方法:</b> クレジットカード (Stripe)</p>
        <br><br>
        <a href="/" style="color:#39FF14; text-decoration:none; border:1px solid #39FF14; padding:10px;">診断に戻る</a>
    </body>
    </html>
    """

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)