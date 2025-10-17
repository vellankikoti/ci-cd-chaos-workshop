#!/usr/bin/env python3
"""
🚀 Blue-Green Deployment Demo App
Simple Flask app that displays version information

Blue-Green Deployment Demo App
"""
from flask import Flask, jsonify, render_template_string
import os
import socket

app = Flask(__name__)

# Get version from environment variable
VERSION = os.getenv('VERSION', 'unknown')
COLOR = os.getenv('COLOR', 'gray')
POD_NAME = os.getenv('POD_NAME', socket.gethostname())

# HTML template with beautiful UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blue-Green Demo - {{ version }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            {% if color == 'blue' %}
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            {% elif color == 'green' %}
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            {% else %}
            background: linear-gradient(135deg, #434343 0%, #000000 100%);
            {% endif %}
            padding: 20px;
        }

        .container {
            background: white;
            border-radius: 20px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            text-align: center;
            max-width: 600px;
            width: 100%;
            animation: slideIn 0.5s ease-out;
        }

        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .version-badge {
            display: inline-block;
            {% if color == 'blue' %}
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            {% elif color == 'green' %}
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            {% else %}
            background: linear-gradient(135deg, #434343 0%, #000000 100%);
            {% endif %}
            color: white;
            padding: 20px 40px;
            border-radius: 50px;
            font-size: 2.5em;
            font-weight: bold;
            margin: 20px 0;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .info-box {
            background: #f7f7f7;
            border-radius: 10px;
            padding: 30px;
            margin: 30px 0;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 0;
            border-bottom: 2px solid #e0e0e0;
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .info-label {
            font-weight: 600;
            color: #555;
            font-size: 1.1em;
        }

        .info-value {
            font-family: 'Courier New', monospace;
            background: white;
            padding: 8px 16px;
            border-radius: 5px;
            color: #333;
            font-size: 0.95em;
        }

        .status {
            margin: 20px 0;
        }

        .status-badge {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border-radius: 20px;
            font-size: 1em;
            display: inline-flex;
            align-items: center;
            gap: 10px;
        }

        .pulse {
            width: 12px;
            height: 12px;
            background: #fff;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% {
                opacity: 1;
            }
            50% {
                opacity: 0.3;
            }
        }

        h1 {
            color: #333;
            margin-bottom: 10px;
            font-size: 2em;
        }

        .subtitle {
            color: #777;
            font-size: 1.1em;
            margin-bottom: 30px;
        }

        .feature-list {
            text-align: left;
            margin: 30px 0;
            padding: 20px;
            background: #f0f0f0;
            border-radius: 10px;
        }

        .feature-item {
            padding: 10px 0;
            color: #555;
            font-size: 1em;
        }

        .feature-item::before {
            content: "✓ ";
            color: #4CAF50;
            font-weight: bold;
            margin-right: 10px;
        }

        .refresh-notice {
            margin-top: 30px;
            color: #999;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Blue-Green Deployment</h1>
        <p class="subtitle">Zero-Downtime Deployment Strategy</p>

        <div class="version-badge">{{ version }}</div>

        <div class="status">
            <div class="status-badge">
                <div class="pulse"></div>
                <span>Service Running</span>
            </div>
        </div>

        <div class="info-box">
            <div class="info-item">
                <span class="info-label">🎨 Environment</span>
                <span class="info-value">{{ color|upper }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">🏷️ Version</span>
                <span class="info-value">{{ version }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">🔧 Pod Name</span>
                <span class="info-value">{{ pod_name }}</span>
            </div>
            <div class="info-item">
                <span class="info-label">🌐 Hostname</span>
                <span class="info-value">{{ hostname }}</span>
            </div>
        </div>

        <div class="feature-list">
            <div class="feature-item">Zero-downtime deployments</div>
            <div class="feature-item">Instant rollback capability</div>
            <div class="feature-item">Two identical production environments</div>
            <div class="feature-item">Traffic switching at load balancer</div>
        </div>

        <p class="refresh-notice">
            🔄 Auto-refresh every 3 seconds
        </p>
    </div>

    <script>
        // Auto-refresh every 3 seconds to show pod changes
        setTimeout(() => location.reload(), 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main page showing version and pod information"""
    return render_template_string(
        HTML_TEMPLATE,
        version=VERSION,
        color=COLOR,
        pod_name=POD_NAME,
        hostname=socket.gethostname()
    )

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': VERSION,
        'color': COLOR,
        'pod_name': POD_NAME,
        'hostname': socket.gethostname()
    })

@app.route('/api/info')
def info():
    """API endpoint returning deployment information"""
    return jsonify({
        'version': VERSION,
        'color': COLOR,
        'pod_name': POD_NAME,
        'hostname': socket.gethostname(),
        'strategy': 'blue-green'
    })

if __name__ == '__main__':
    print(f"""
╔════════════════════════════════════════════════════════════╗
║  🚀 Blue-Green Deployment Demo App                        ║
║  Version: {VERSION:<48} ║
║  Color: {COLOR:<50} ║
╚════════════════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=8080, debug=False)
