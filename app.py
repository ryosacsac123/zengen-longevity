from flask import Flask, send_file, request, jsonify
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
import os
import io

app = Flask(__name__)

# --- 1. あなたの「完璧な」PDFデザインロジック (完全復元) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # 1ページ目：漆黒の背景とネオングリーンのデザイン
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    
    p.setFont("Helvetica-Bold", 10)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "OFFICIAL LONGEVITY BLUEPRINT")
    
    # スコアの円形デザイン
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(3)
    p.circle(width/2, height - 150, 70, stroke=1, fill=0)
    
    p.setFont("Helvetica-Bold", 40)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 165, f"{score}/8")
    
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 240, "JDI8 SCORE")
    
    # リスク評価ロジック
    if score <= 3: risk_text = "RISK ASSESSMENT: HIGH"
    elif score <= 6: risk_text = "RISK ASSESSMENT: MODERATE"
    else: risk_text = "RISK ASSESSMENT: LOW"

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 270, risk_text)

    # セクション02: Genetic Edge
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 330, "02 // THE JAPANESE GENETIC EDGE")
    p.setFont("Helvetica", 10)
    p.setFillColor(colors.white)
    p.drawString(40, height - 350, "Nature (2010): Porphyranase enzyme pathway identified for marine processing.")

    # セクション03: Protocol (テーブル)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 390, "03 // PERSONALIZED PROTOCOL")

    # 水曜日のSeaweed表現を含むデータ
    seaweed_text = "Seaweed side dish. Support marine polysaccharide digestion."
    if score <= 4:
        data = [
            ["Day", "Focus", "Action"],
            ["Mon", "Autophagy", "Hydration focus. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "Eat Natto at dinner to support mucosa."],
            ["Wed", "Enzyme", seaweed_text],
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

    p.showPage() # 2ページ目 (Amazonリンク)
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(40, height - 40, "04 // THE GOLD STANDARD STACK")

    # 商品リスト
    items = [
        ("Ippodo Matcha", "Finest L-Theanine source.", "https://amzn.to/3ZgMv0Q"),
        ("NMN", "NAD+ precursor for repair.", "https://amzn.to/4qTcOHM"),
        ("Spermidine", "Autophagy inducer.", "https://amzn.to/4tYE6j2"),
        ("EPA/DHA", "Inflammation control.", "https://amzn.to/4kRTklz"),
        ("Zojirushi IH", "Metabolism foundation.", "https://amzn.to/4hfC1sA")
    ]
    y_pos = height - 80
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

# --- 2. ルート設定 (サーバー起動前にすべて定義します) ---

@app.route('/')
def home():
    # 診断を開始するトップ画面
    return """
    <html>
    <head>
        <title>ZENGEN AI</title>
        <style>
            body { background:#000; color:#fff; font-family:sans-serif; text-align:center; padding-top:10vh; }
            h1 { color:#39FF14; font-size:3rem; letter-spacing:5px; margin-bottom:5px; }
            .tag { color:#888; font-style:italic; margin-bottom:40px; }
            .card { background:#111; border:1px solid #333; padding:30px; border-radius:15px; display:inline-block; text-align:left; box-shadow:0 10px 30px rgba(0,0,0,0.5); }
            .q { margin-bottom:15px; font-size:1.1rem; display:flex; align-items:center; }
            input[type="checkbox"] { transform:scale(1.5); margin-right:15px; accent-color:#39FF14; }
            button { width:100%; background:#39FF14; color:#000; border:none; padding:15px; font-weight:bold; cursor:pointer; margin-top:20px; font-size:1.1rem; }
            button:hover { background:#fff; }
            footer { margin-top:50px; font-size:0.7rem; color:#444; }
            footer a { color:#444; text-decoration:none; }
        </style>
    </head>
    <body>
        <h1>ZENGEN AI</h1>
        <p class="tag">Longevity Protocol Engine</p>
        <div class="card">
            <div class="q"><input type="checkbox" class="j"> Rice (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Miso Soup (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Seaweed (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Pickles (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Green & Yellow Veg (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Fish (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Green Tea (Daily)</div>
            <div class="q"><input type="checkbox" class="j"> Low Beef/Pork Intake</div>
            <button onclick="calc()">GET PREMIUM REPORT ($5)</button>
        </div>
        <script>
            function calc() {
                let score = document.querySelectorAll('.j:checked').length;
                window.location.href = '/download-report?score=' + score;
            }
        </script>
        <footer><a href="/legal">Commerce Disclosure (特定商取引法に基づく表記)</a></footer>
    </body>
    </html>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    pdf_buffer = create_report(score)
    return send_file(pdf_buffer, as_attachment=True, download_name=f"ZENGEN_Report_{score}.pdf", mimetype='application/pdf')

@app.route('/legal')
def legal():
    return """
    <body style="background:#000; color:#fff; font-family:sans-serif; padding:40px; line-height:1.8;">
        <h1 style="color:#39FF14;">特定商取引法に基づく表記</h1>
        <p><b>販売業者:</b> 佐久間稜</p>
        <p><b>所在地:</b> 〒060-0813 北海道札幌市北区北13条西8丁目 北海道大学大学院 工学院</p>
        <p><b>電話番号:</b> 090-6446-6654</p>
        <p><b>販売価格:</b> $5.00</p>
        <br><a href="/" style="color:#39FF14; text-decoration:none; border:1px solid #39FF14; padding:10px;">診断に戻る</a>
    </body>
    </html>
    """

# --- 3. サーバー起動 (必ず一番最後に置く) ---
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)