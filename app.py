from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)


HTML = """
<!DOCTYPE html>
<html lang="sq">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>CI/CD Pipeline — Live Demo</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;800&display=swap" rel="stylesheet"/>
<style>
  :root {
    --bg: #050810;
    --border: #1a2540;
    --accent: #00e5ff;
    --accent2: #7c3aed;
    --text: #e8eaf6;
    --muted: #4a5580;
    --font-display: 'Syne', sans-serif;
    --font-mono: 'Space Mono', monospace;
  }

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-mono);
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    overflow-x: hidden;
  }

  body::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
      linear-gradient(rgba(0,229,255,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,229,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
  }

  body::after {
    content: '';
    position: fixed;
    top: -200px;
    left: 50%;
    transform: translateX(-50%);
    width: 800px;
    height: 600px;
    background: radial-gradient(ellipse, rgba(124,58,237,0.15) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    width: 100%;
    padding: 24px;
    text-align: center;
  }

  header {
    animation: fadeDown 0.8s ease both;
  }

  .badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,229,255,0.08);
    border: 1px solid rgba(0,229,255,0.2);
    color: var(--accent);
    font-size: 11px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    padding: 6px 14px;
    border-radius: 2px;
    margin-bottom: 28px;
  }

  .badge-dot {
    width: 6px; height: 6px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse 1.5s ease infinite;
  }

  h1.title {
    font-family: var(--font-display);
    font-size: clamp(40px, 7vw, 80px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 70%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 20px;
  }

  .subtitle {
    color: var(--muted);
    font-size: 13px;
    letter-spacing: 0.05em;
    line-height: 1.9;
  }

  .thankyou {
    margin-top: 60px;
    animation: fadeUp 1s ease both;
  }

  @keyframes fadeDown {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to   { opacity: 1; transform: translateY(0); }
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
  }
</style></head>
<body>
<div class="container">

  <header>
    <div class="badge">
      <span class="badge-dot"></span>
      Live Demo — Prezantim
    </div>
    <h1 class="title">CI/CD Pipeline<br/>Automation</h1>
    <p class="subtitle">
      Integrimi dhe shpërndarja e vazhdueshme —<br/>
      nga commit-i deri në production, automatikisht.
    </p>
  </header>

  <div class="thankyou">
    <!-- <h1 class="faleminderit" style="font-family:'Syne',sans-serif;font-size:clamp(48px,8vw,96px);font-weight:800;background:linear-gradient(135deg,#fff 20%,#00e5ff 60%,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.03em;">Faleminderit</h1> -->
  </div>

</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)