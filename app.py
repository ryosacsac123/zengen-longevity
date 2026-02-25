import os
import io
import stripe
from flask import Flask, send_file, request, jsonify, redirect
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

app = Flask(__name__)

# --- COMMERCIAL GATEKEEPING ---
# Set to True for Stripe Review (Locks PDF behind payment)
# Set to False only for your own testing (Bypasses payment)
COMMERCIAL_READY = True 

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "sk_test_placeholder")

# --- 1. ENHANCED PDF ENGINE (Ryoh Sakuma Design) ---
def create_report(score):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # --- PAGE 1: DIAGNOSIS & ARCHITECTURE --- [cite: 7-14, 24-31]
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 12)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(50, height - 50, "OFFICIAL LONGEVITY BLUEPRINT // ZENGEN AI")
    
    # Large Biometric Score Circle
    p.setStrokeColor(colors.HexColor("#39FF14"))
    p.setLineWidth(4)
    p.circle(width/2, height - 180, 85, stroke=1, fill=0)
    p.setFont("Helvetica-Bold", 55)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 200, f"{score}/8")
    
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawCentredString(width/2, height - 290, "JDI8 BIOMETRIC SCORE")
    
    risk = "HIGH" if score <= 3 else "MODERATE" if score <= 6 else "LOW"
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.white)
    p.drawCentredString(width/2, height - 330, f"RISK ASSESSMENT: {risk}")

    p.setStrokeColor(colors.HexColor("#333333"))
    p.line(50, height - 360, width - 50, height - 360)

    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(50, height - 400, "02 // SCIENTIFIC FOUNDATION")
    p.setFont("Helvetica", 11)
    p.setFillColor(colors.white)
    p.drawString(50, height - 425, "Source: Nature (2010). Human gut bacterial metabolism of red seaweed.")
    p.drawString(50, height - 440, "Porphyranase enzyme pathway specialized for marine polysaccharide processing.")

    # Protocol Table [cite: 7, 31]
    p.setFont("Helvetica-Bold", 14)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(50, height - 480, "03 // 7-DAY PERSONALIZED PROTOCOL")

    data = [["Day", "Focus", "Action Plan"]]
    if score <= 4:
        rows = [
            ["Mon", "Autophagy", "Strict 16:8 Fasting. Start with Miso soup to reset."],
            ["Tue", "Microbiome", "High-density Natto intake for mucosal support."],
            ["Wed", "Enzyme", "Red seaweed integration. Activate Porphyranase."],
            ["Thu", "Recovery", "2g Premium Ippodo Matcha. Prioritize L-Theanine."],
            ["Fri", "Omega-3", "1g EPA/DHA. Optimize inflammation control."],
            ["Sat", "Metabolism", "HIIT Session (20min). Activate cellular glycolysis."],
            ["Sun", "Rest", "Hot soak (42C) followed by 2min cold exposure."]
        ]
    else:
        rows = [
            ["Mon", "Reset", "Autophagy initiation. Miso & Seaweed protocol."],
            ["Tue", "Diversity", "Mix Natto with fermented fibers (Kimchi/Okra)."],
            ["Wed", "Catalyst", "Seaweed salad. Maximize marine polysaccharide conversion."],
            ["Thu", "Nootropic", "3g Ippodo Matcha. Focus on cognitive NAD+ repair."],
            ["Fri", "Lipids", "Wild-caught fatty fish + EPA supplement."],
            ["Sat", "Vascular", "Zone 2 Cardio (45min). Mitochondrial biogenesis."],
            ["Sun", "Homeostasis", "Deep tissue recovery + Magnesium-rich bath."]
        ]
    for r in rows: data.append(r)

    table = Table(data, colWidths=[60, 90, 340], rowHeights=25)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1A1A1A")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#39FF14")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#333333")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    table.wrapOn(p, 50, 420)
    table.drawOn(p, 50, height - 680)

    # --- PAGE 2: THE GOLD STANDARD STACK --- 
    p.showPage()
    p.setFillColor(colors.black)
    p.rect(0, 0, width, height, fill=1)
    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.HexColor("#39FF14"))
    p.drawString(50, height - 60, "04 // THE GOLD STANDARD STACK")

    stacks = [
        ("Ippodo Matcha", "Highest concentration of L-Theanine for neuroprotection.", "https://amzn.to/3ZgMv0Q"),
        ("Suntory NMN", "NAD+ precursor. 99.9% purity for cellular DNA repair.", "https://amzn.to/4qTcOHM"),
        ("Spermidine", "Natural polyamine that triggers cellular autophagy.", "https://amzn.to/4tYE6j2"),
        ("High-Dose EPA/DHA", "Advanced inflammation and cardiovascular control.", "https://amzn.to/4kRTklz"),
        ("Zojirushi IH Engine", "Standard for consistent glycaemic index control.", "https://amzn.to/4hfC1sA")
    ]
    
    y = height - 140
    for title, desc, link in stacks:
        p.setStrokeColor(colors.HexColor("#222222"))
        p.rect(50, y - 55, width - 100, 70, stroke=1, fill=0)
        p.setFont("Helvetica-Bold", 13)
        p.setFillColor(colors.white)
        p.drawString(65, y, f"> {title}")
        p.setFont("Helvetica", 10)
        p.setFillColor(colors.lightgrey)
        p.drawString(65, y - 18, desc)
        p.setFont("Helvetica-Oblique", 9)
        p.setFillColor(colors.HexColor("#39FF14"))
        p.drawString(65, y - 38, f"Purchase via Amazon: {link}")
        y -= 90
    
    p.setFont("Helvetica", 8)
    p.setFillColor(colors.HexColor("#444444"))
    p.drawCentredString(width/2, 40, "DEVELOPED BY RYOH SAKUMA // HOKKAIDO UNIVERSITY // ADVICE ONLY")
    
    p.save()
    buffer.seek(0)
    return buffer

# --- 2. WEB INTERFACE (Premium Page 3) ---

@app.route('/')
def home():
    ready_js = "true" if COMMERCIAL_READY else "false"
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>ZENGEN AI | Longevity</title>
        <style>
            :root { --neon: #39FF14; --bg: #000; }
            body { margin:0; overflow:hidden; background:var(--bg); color:#fff; font-family:'Inter', sans-serif; }
            #canvas { position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; filter:blur(40px); opacity:0.8; }
            .screen { position:absolute; width:100vw; height:100vh; display:flex; flex-direction:column; align-items:center; justify-content:center; transition:0.9s cubic-bezier(0.8, 0, 0.2, 1); }
            #page1 { transform:translateX(0); }
            #page2 { transform:translateX(100%); }
            #page3 { transform:translateX(100%); }
            h1 { font-size:6.5rem; letter-spacing:25px; color:var(--neon); font-weight:100; margin:0; text-shadow:0 0 30px var(--neon); cursor:pointer; }
            .card { background:rgba(10,10,10,0.85); border:1px solid #222; padding:55px; border-radius:35px; backdrop-filter:blur(30px); width:540px; box-shadow:0 60px 120px #000; position:relative; }
            .section-label { color:var(--neon); font-size:0.7rem; letter-spacing:5px; margin-bottom:20px; text-transform:uppercase; border-bottom:1px solid #222; padding-bottom:10px; }
            .q-item { margin-bottom:15px; display:flex; align-items:center; font-size:1.15rem; color:#ccc; cursor:pointer; }
            input[type="checkbox"] { transform:scale(1.7); margin-right:20px; accent-color:var(--neon); }
            button { background:transparent; color:var(--neon); border:1px solid var(--neon); padding:20px 75px; font-weight:bold; cursor:pointer; letter-spacing:6px; transition:0.6s; margin-top:40px; text-transform:uppercase; }
            button:hover { background:var(--neon); color:#000; box-shadow:0 0 50px var(--neon); }
            .summary-box { border-left: 2px solid var(--neon); padding-left: 25px; margin: 35px 0; text-align: left; }
            .risk-tag { display:inline-block; padding:5px 15px; border-radius:5px; font-size:0.8rem; font-weight:bold; margin-bottom:10px; }
            .high { background:rgba(255,0,0,0.2); color:#ff4444; border:1px solid #ff4444; }
            .mod { background:rgba(255,165,0,0.2); color:#ffa500; border:1px solid #ffa500; }
            .low { background:rgba(57,255,20,0.2); color:var(--neon); border:1px solid var(--neon); }
            .value-header { color:var(--neon); font-size:0.75rem; letter-spacing:3px; margin-top:25px; margin-bottom:10px; font-weight:bold; }
            .val-list { list-style: none; padding: 0; color: #888; font-size: 0.95rem; line-height: 2.1; }
            .val-list b { color: #eee; }
            .disclaimer { position:absolute; bottom:20px; width:100%; text-align:center; font-size:0.55rem; color:#444; letter-spacing:1.1px; }
        </style>
    </head>
    <body>
        <canvas id="canvas"></canvas>
        <div id="page1" class="screen">
            <h1 onclick="move(1,2)">ZENGEN</h1>
            <button onclick="move(1,2)">Initiate Analysis</button>
            <div class="disclaimer">ADVICE ONLY. NOT A MEDICAL DIAGNOSIS. DEVELOPED BY RYOH SAKUMA.</div>
        </div>
        <div id="page2" class="screen">
            <div class="card">
                <div class="section-label">02 // BIOMETRIC INPUT</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> RICE (DAILY)</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> MISO SOUP (DAILY)</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> SEAWEED (DAILY)</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> PICKLES (DAILY)</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> GREEN & YELLOW VEG</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> FISH (DAILY)</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j"> GREEN TEA (DAILY)</div>
                <div class="section-label" style="margin-top:30px;">02b // INVERSE FACTOR</div>
                <div class="q-item" onclick="this.querySelector('input').click()"><input type="checkbox" class="j-inv"> LOW BEEF/PORK INTAKE</div>
                <button onclick="move(2,3)" style="width:100%;">Synthesize Protocol</button>
            </div>
            <div class="disclaimer">ADVICE ONLY. NOT A MEDICAL DIAGNOSIS.</div>
        </div>
        <div id="page3" class="screen">
            <div class="card" style="text-align:center;">
                <div class="section-label">03 // ANALYSIS COMPLETE</div>
                <h2 style="letter-spacing:10px; font-weight:100; font-size:2.2rem; margin:0;">BIOMETRIC REPORT</h2>
                <div class="summary-box">
                    <div id="riskTag" class="risk-tag">ASSESSING...</div>
                    <div style="font-size: 1.6rem; letter-spacing: 2px;">JDI8 Score: <span id="dispScore" style="color:var(--neon); font-weight:bold;">0</span>/8</div>
                    <p id="riskDesc" style="color:#777; font-size:0.9rem; margin-top:10px; line-height:1.6;"></p>
                    
                    <div class="value-header">UPON UNLOCKING, YOU RECEIVE:</div>
                    <ul class="val-list">
                        <li>● <b>7-Day Precision Protocol:</b> Tailored meal & habit timings.</li>
                        <li>● <b>Enzyme Catalyst Guide:</b> How to trigger marine enzyme pathways.</li>
                        <li>● <b>Architectural Stack:</b> Direct links to 99.9% pure NAD+ precursors.</li>
                        <li>● <b>DNA Repair Guide:</b> Scientific heat/cold exposure protocols.</li>
                    </ul>
                </div>
                <form id="payForm" action="/create-checkout-session" method="POST">
                    <input type="hidden" name="score" id="scoreInput" value="0">
                    <button type="submit" id="mainBtn" style="width:100%; border:none; background:var(--neon); color:#000;">Unlock Full Architecture ($5.00)</button>
                </form>
                <div style="margin-top:25px; font-size:0.75rem;"><a href="/about" style="color:#555; text-decoration:none;">ABOUT US</a> | <a href="/legal" style="color:#555; text-decoration:none;">COMMERCE DISCLOSURE</a></div>
            </div>
        </div>
        <script>
            const canvas = document.getElementById('canvas'); const ctx = canvas.getContext('2d');
            let w, h, orbs = [], state = "dance", isCommercial = DEBUG_REPLACE;
            function init() {
                w = canvas.width = window.innerWidth; h = canvas.height = window.innerHeight;
                orbs = []; for(let i=0; i<15; i++) orbs.push({x:Math.random()*w, y:Math.random()*h, r:Math.random()*200+100, v:{x:(Math.random()-0.5)*0.6, y:(Math.random()-0.5)*0.6}});
            }
            function draw() {
                ctx.clearRect(0,0,w,h);
                orbs.forEach(o => {
                    if(state === "dance") { o.x += o.v.x; o.y += o.v.y; if(o.x<0||o.x>w) o.v.x*=-1; if(o.y<0||o.y>h) o.v.y*=-1; }
                    else { o.x += (w/2 - o.x) * 0.02; o.y += (h/2 - o.y) * 0.02; o.r += (150 - o.r) * 0.01; }
                    let g = ctx.createRadialGradient(o.x,o.y,0,o.x,o.y,o.r); g.addColorStop(0,'rgba(57,255,20,0.4)'); g.addColorStop(1,'rgba(0,0,0,0)');
                    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(o.x,o.y,o.r,0,Math.PI*2); ctx.fill();
                }); requestAnimationFrame(draw);
            }
            init(); draw();
            function move(f, t) {
                if(f===1) state = "converge"; 
                let s = document.querySelectorAll('.j:checked').length + document.querySelectorAll('.j-inv:checked').length;
                document.getElementById('dispScore').innerText = s;
                document.getElementById('scoreInput').value = s;
                const tag = document.getElementById('riskTag'); const desc = document.getElementById('riskDesc');
                if(s <= 3) { tag.innerText = "HIGH RISK"; tag.className = "risk-tag high"; desc.innerText = "Biological indicators suggest a lack of traditional genetic triggers. Protocol implementation recommended."; }
                else if(s <= 6) { tag.innerText = "MODERATE RISK"; tag.className = "risk-tag mod"; desc.innerText = "Dietary index is stable but lacks specific marine enzyme activation for optimal NAD+ repair."; }
                else { tag.innerText = "LOW RISK"; tag.className = "risk-tag low"; desc.innerText = "Exceptional biological alignment. Blueprint recommended for fine-tuning NAD+ precursors."; }
                if(!isCommercial) { document.getElementById('mainBtn').innerText = "TEST: DOWNLOAD PDF"; document.getElementById('payForm').onsubmit = (e) => { e.preventDefault(); window.location.href = "/download-report?score=" + s; }; }
                document.getElementById('page'+f).style.transform = 'translateX(-100%)';
                document.getElementById('page'+t).style.transform = 'translateX(0)';
            }
        </script>
    </body>
    </html>
    """.replace("DEBUG_REPLACE", ready_js)
    return html

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    score = request.form.get('score', 0)
    try:
        session = stripe.checkout.Session.create(
            line_items=[{'price_data': {'currency': 'usd', 'product_data': {'name': 'ZENGEN Longevity Blueprint'}, 'unit_amount': 500}, 'quantity': 1}],
            mode='payment',
            success_url=request.host_url + f'success?score={score}',
            cancel_url=request.host_url,
        )
        return redirect(session.url, code=303)
    except Exception as e: return str(e), 500

@app.route('/success')
def success():
    score = request.args.get('score', 0)
    return f"""
    <body style="background:#000; color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center; height:100vh; font-family:sans-serif; margin:0;">
        <h2 style="color:#39FF14; letter-spacing:5px;">PAYMENT SUCCESSFUL</h2>
        <a href="/download-report?score={score}" style="text-decoration:none; background:#39FF14; color:#000; padding:20px 40px; font-weight:bold; border-radius:5px; margin-top:30px;">
            DOWNLOAD OFFICIAL LONGEVITY BLUEPRINT
        </a>
    </body>
    """

@app.route('/download-report')
def download_report():
    score = int(request.args.get('score', 0))
    return send_file(create_report(score), as_attachment=True, download_name=f"ZENGEN_Official_Report.pdf", mimetype='application/pdf')

@app.route('/about')
def about():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.8;"><h1 style="color:#39FF14;">ABOUT US</h1><p>Curated by Ryoh Sakuma, Hokkaido University Graduate School of Engineering.</p><a href="/" style="color:#39FF14;">BACK</a></body>"""

@app.route('/legal')
def legal():
    return """<body style="background:#000;color:#fff;padding:80px;font-family:sans-serif;line-height:2.8;"><h1 style="color:#39FF14;">COMMERCE DISCLOSURE</h1><p>Merchant: Ryoh Sakuma<br>Location: Sapporo, Japan (Hokkaido University)<br>Price: $5.00<br>Contact: ryo1ryo2-1103@outlook.jp</p><a href="/" style="color:#39FF14;">BACK</a></body>"""

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)