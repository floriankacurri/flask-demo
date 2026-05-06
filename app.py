from flask import Flask, jsonify, render_template_string
from datetime import datetime
import random

app = Flask(__name__)

PIPELINE_STAGES = [
    {"id": 1, "name": "Code Push", "icon": "⬆", "description": "Zhvilluesi bën push në GitHub"},
    {"id": 2, "name": "Lint & Format", "icon": "✦", "description": "Kontrolli i stilit të kodit"},
    {"id": 3, "name": "Unit Tests", "icon": "◈", "description": "Ekzekutimi i testeve automatike"},
    {"id": 4, "name": "Build", "icon": "⬡", "description": "Ndërtimi i artefaktit"},
    {"id": 5, "name": "Deploy", "icon": "◎", "description": "Shpërndarje automatike në prodhim"},
]

METRICS = {
    "deployments_today": 0,
    "tests_passed": 0,
    "uptime": "99.98%",
    "avg_pipeline_time": "2m 34s",
}

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
    --surface: #0c1120;
    --border: #1a2540;
    --accent: #00e5ff;
    --accent2: #7c3aed;
    --success: #00ff87;
    --warn: #ffbe0b;
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
    overflow-x: hidden;
  }

  /* Grid background */
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

  /* Glow orb */
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
    max-width: 1100px;
    margin: 0 auto;
    padding: 40px 24px 80px;
  }

  /* Header */
  header {
    text-align: center;
    padding: 60px 0 50px;
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
    font-size: clamp(36px, 6vw, 72px);
    font-weight: 800;
    line-height: 1.05;
    letter-spacing: -0.03em;
    background: linear-gradient(135deg, #fff 30%, var(--accent) 70%, var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 16px;
  }

  .subtitle {
    color: var(--muted);
    font-size: 13px;
    letter-spacing: 0.05em;
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.8;
  }

  /* Metrics row */
  .metrics {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 40px;
    animation: fadeUp 0.8s 0.2s ease both;
  }

  .metric {
    background: var(--surface);
    padding: 24px 20px;
    text-align: center;
    transition: background 0.2s;
  }

  .metric:hover { background: #101828; }

  .metric-value {
    font-family: var(--font-display);
    font-size: 32px;
    font-weight: 800;
    color: var(--accent);
    display: block;
    margin-bottom: 4px;
  }

  .metric-label {
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
  }

  /* Pipeline */
  .section-title {
    font-family: var(--font-display);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  .pipeline {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    margin-bottom: 40px;
    animation: fadeUp 0.8s 0.3s ease both;
  }

  .stage {
    background: var(--surface);
    padding: 28px 16px;
    text-align: center;
    position: relative;
    cursor: default;
    transition: background 0.25s;
  }

  .stage:hover { background: #101828; }

  .stage.active { background: rgba(0,229,255,0.05); }
  .stage.active .stage-icon { color: var(--accent); }
  .stage.active .stage-status { background: rgba(0,229,255,0.15); color: var(--accent); }

  .stage.done .stage-icon { color: var(--success); }
  .stage.done .stage-status { background: rgba(0,255,135,0.1); color: var(--success); }

  .stage-num {
    font-size: 10px;
    color: var(--muted);
    letter-spacing: 0.1em;
    margin-bottom: 12px;
  }

  .stage-icon {
    font-size: 28px;
    display: block;
    margin-bottom: 12px;
    color: var(--muted);
    transition: color 0.3s;
  }

  .stage-name {
    font-family: var(--font-display);
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 6px;
    color: var(--text);
  }

  .stage-desc {
    font-size: 10px;
    color: var(--muted);
    line-height: 1.6;
    margin-bottom: 14px;
  }

  .stage-status {
    display: inline-block;
    font-size: 9px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 8px;
    border-radius: 2px;
    background: rgba(74,85,128,0.2);
    color: var(--muted);
    transition: all 0.3s;
  }

  /* Connector arrows between stages */
  .stage:not(:last-child)::after {
    content: '→';
    position: absolute;
    right: -10px;
    top: 50%;
    transform: translateY(-50%);
    color: var(--muted);
    font-size: 14px;
    z-index: 2;
    background: var(--border);
    padding: 2px 1px;
  }

  /* Simulate button */
  .controls {
    display: flex;
    gap: 12px;
    margin-bottom: 40px;
    animation: fadeUp 0.8s 0.4s ease both;
  }

  .btn {
    font-family: var(--font-mono);
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 12px 24px;
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    cursor: pointer;
    transition: all 0.2s;
    border-radius: 2px;
  }

  .btn:hover { border-color: var(--accent); color: var(--accent); }

  .btn-primary {
    background: var(--accent);
    color: #000;
    border-color: var(--accent);
    font-weight: 700;
  }

  .btn-primary:hover { background: #00c4db; color: #000; border-color: #00c4db; }
  .btn-primary:disabled { opacity: 0.4; cursor: not-allowed; }

  /* Log terminal */
  .log-section { animation: fadeUp 0.8s 0.5s ease both; }

  .terminal {
    background: #020408;
    border: 1px solid var(--border);
    border-radius: 2px;
    overflow: hidden;
  }

  .terminal-header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .terminal-dots { display: flex; gap: 6px; }
  .dot { width: 10px; height: 10px; border-radius: 50%; }
  .dot-r { background: #ff5f57; }
  .dot-y { background: #febc2e; }
  .dot-g { background: #28c840; }

  .terminal-title {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.1em;
  }

  .terminal-body {
    padding: 20px;
    min-height: 200px;
    max-height: 320px;
    overflow-y: auto;
    font-size: 12px;
    line-height: 2;
  }

  .log-line {
    display: flex;
    gap: 12px;
    opacity: 0;
    animation: logAppear 0.3s ease forwards;
  }

  .log-time { color: var(--muted); min-width: 80px; }
  .log-msg { color: #a8c8ff; }
  .log-msg.success { color: var(--success); }
  .log-msg.error { color: #ff4d6d; }
  .log-msg.warn { color: var(--warn); }
  .log-msg.info { color: var(--accent); }

  /* Thank you */
  .thankyou {
    text-align: center;
    padding: 60px 0 20px;
    animation: fadeUp 1s ease both;
  }

  /* h1.faleminderit { display: none; } */

  /* Footer */
  footer {
    text-align: center;
    padding: 40px 0 0;
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.08em;
    border-top: 1px solid var(--border);
    margin-top: 60px;
  }

  /* Animations */
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
  @keyframes logAppear {
    to { opacity: 1; }
  }
  @keyframes spin {
    to { transform: rotate(360deg); }
  }

  .spinner {
    display: inline-block;
    width: 12px; height: 12px;
    border: 2px solid var(--muted);
    border-top-color: var(--accent);
    border-radius: 50%;
    animation: spin 0.7s linear infinite;
    vertical-align: middle;
    margin-right: 6px;
  }

  @media (max-width: 768px) {
    .metrics { grid-template-columns: repeat(2, 1fr); }
    .pipeline { grid-template-columns: 1fr; }
    .stage:not(:last-child)::after { content: '↓'; right: 50%; top: auto; bottom: -12px; transform: translateX(50%); }
  }
</style>
</head>
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
     <h1 class="faleminderit" style="font-family:'Syne',sans-serif;font-size:clamp(48px,8vw,96px);font-weight:800;background:linear-gradient(135deg,#fff 20%,#00e5ff 60%,#7c3aed);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:-0.03em;">Faleminderit</h1>
  </div>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        stages=PIPELINE_STAGES,
        metrics=METRICS,
        year=datetime.now().year
    )

@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200

@app.route("/api/metrics")
def metrics():
    METRICS["deployments_today"] = random.randint(12, 40)
    METRICS["tests_passed"] = random.randint(200, 500)
    return jsonify(METRICS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)