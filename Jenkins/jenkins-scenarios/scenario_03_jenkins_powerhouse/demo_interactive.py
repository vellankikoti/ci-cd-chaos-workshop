#!/usr/bin/env python3
"""
Jenkins Powerhouse - Interactive Demo
====================================

Interactive demonstration of Jenkins advanced features with web applications.
Shows the power of Jenkins plugins, advanced pipelines, and optimization through visual comparison.

This is the interactive version of the main demo.py for advanced users.
Use demo.py for the standard interactive experience.

Usage:
    python3 demo_interactive.py
"""

import time
import threading
import subprocess
import sys
import os
import signal
import webbrowser
from pathlib import Path

class Colors:
    """Color support for terminal output."""
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

class JenkinsPowerhouseDemo:
    """Interactive Jenkins powerhouse demonstration."""
    
    def __init__(self):
        self.processes = []
        self.running = True
        
    def print_header(self, message):
        """Print a header message."""
        print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")
        
    def print_step(self, message):
        """Print a step message."""
        print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")
        
    def print_success(self, message):
        """Print a success message."""
        print(f"{Colors.GREEN}✅ {message}{Colors.NC}")
        
    def print_info(self, message):
        """Print an info message."""
        print(f"{Colors.CYAN}ℹ️  {message}{Colors.NC}")
        
    def print_warning(self, message):
        """Print a warning message."""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.NC}")
        
    def print_error(self, message):
        """Print an error message."""
        print(f"{Colors.RED}❌ {message}{Colors.NC}")
        
    def run_command(self, cmd, description=""):
        """Run a command with error handling."""
        if description:
            self.print_step(description)
            
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                self.print_error(f"Command failed: {result.stderr}")
                return False
        except Exception as e:
            self.print_error(f"Error running command: {e}")
            return False
    
    def start_application(self, app_name, port, description):
        """Start a web application."""
        self.print_step(f"Starting {app_name} on port {port}")
        
        try:
            # Create the application file if it doesn't exist
            app_file = f"{app_name.lower().replace(' ', '_')}_app.py"
            if not os.path.exists(app_file):
                self.create_demo_app(app_file, app_name, port)
            
            # Start the application
            process = subprocess.Popen(
                [sys.executable, app_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            self.processes.append(process)
            self.print_success(f"{app_name} started on http://localhost:{port}")
            return True
            
        except Exception as e:
            self.print_error(f"Failed to start {app_name}: {e}")
            return False
    
    def create_demo_app(self, filename, app_name, port):
        """Create a demo application file."""
        if "dashboard" in app_name.lower():
            content = self.create_dashboard_app(port)
        elif "basic" in app_name.lower():
            content = self.create_basic_jenkins_app(port)
        elif "powerhouse" in app_name.lower():
            content = self.create_powerhouse_jenkins_app(port)
        else:
            content = self.create_basic_app(app_name, port)
            
        with open(filename, 'w') as f:
            f.write(content)
    
    def create_dashboard_app(self, port):
        """Create the Jenkins powerhouse dashboard app."""
        return f'''#!/usr/bin/env python3
"""
Jenkins Powerhouse Dashboard
===========================
Real-time dashboard showing Jenkins advanced features and performance metrics.
"""

from flask import Flask, render_template_string, jsonify
import time
import random
import threading

app = Flask(__name__)

# Dashboard HTML template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Jenkins Powerhouse Dashboard</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
            margin: 10px 0;
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .metric-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }}
        .metric-title {{
            font-size: 1.1em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            margin: 10px 0;
        }}
        .metric-change {{
            font-size: 0.9em;
            opacity: 0.8;
        }}
        .positive {{ color: #4CAF50; }}
        .negative {{ color: #f44336; }}
        .neutral {{ color: #ffd700; }}
        .plugin-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .plugin-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            color: #ffd700;
        }}
        .plugin-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .plugin-card {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #4CAF50;
        }}
        .plugin-name {{
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #4CAF50;
        }}
        .plugin-desc {{
            font-size: 0.9em;
            line-height: 1.5;
            opacity: 0.9;
        }}
        .comparison-section {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .comparison-title {{
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 20px;
            text-align: center;
            color: #ffd700;
        }}
        .comparison-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }}
        .comparison-item {{
            text-align: center;
            padding: 20px;
            border-radius: 10px;
        }}
        .basic-jenkins {{
            background: rgba(244, 67, 54, 0.2);
            border: 2px solid #f44336;
        }}
        .powerhouse-jenkins {{
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid #4CAF50;
        }}
        .jenkins-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 15px;
        }}
        .jenkins-features {{
            list-style: none;
            padding: 0;
            margin: 15px 0;
        }}
        .jenkins-features li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .jenkins-features li:last-child {{
            border-bottom: none;
        }}
        .auto-refresh {{
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0, 0, 0, 0.5);
            padding: 10px;
            border-radius: 5px;
            font-size: 0.9em;
        }}
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        .pulse {{
            animation: pulse 2s infinite;
        }}
    </style>
    <script>
        function updateMetrics() {{
            fetch('/api/metrics')
                .then(response => response.json())
                .then(data => {{
                    document.getElementById('total-builds').textContent = data.total_builds;
                    document.getElementById('success-rate').textContent = data.success_rate + '%';
                    document.getElementById('avg-duration').textContent = data.avg_duration + 's';
                    document.getElementById('plugins-enabled').textContent = data.plugins_enabled;
                    document.getElementById('pipeline-efficiency').textContent = data.pipeline_efficiency + '%';
                    document.getElementById('user-satisfaction').textContent = data.user_satisfaction + '%';
                    document.getElementById('last-updated').textContent = new Date().toLocaleTimeString();
                }})
                .catch(error => console.error('Error updating metrics:', error));
        }}
        
        // Update metrics every 3 seconds
        setInterval(updateMetrics, 3000);
        
        // Initial load
        updateMetrics();
    </script>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Jenkins Powerhouse Dashboard</h1>
            <p>Real-time analytics and advanced features showcase</p>
        </div>
        
        <div class="metrics-grid">
            <div class="metric-card">
                <div class="metric-title">Total Builds</div>
                <div class="metric-value" id="total-builds">0</div>
                <div class="metric-change positive">+25 this hour</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Success Rate</div>
                <div class="metric-value" id="success-rate">0%</div>
                <div class="metric-change positive">+8% improvement</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Avg Duration</div>
                <div class="metric-value" id="avg-duration">0s</div>
                <div class="metric-change negative">-25% faster</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Plugins Enabled</div>
                <div class="metric-value" id="plugins-enabled">0</div>
                <div class="metric-change positive">+400% features</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Pipeline Efficiency</div>
                <div class="metric-value" id="pipeline-efficiency">0%</div>
                <div class="metric-change positive">+60% optimization</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">User Satisfaction</div>
                <div class="metric-value" id="user-satisfaction">0%</div>
                <div class="metric-change positive">+500% improvement</div>
            </div>
            
            <div class="metric-card">
                <div class="metric-title">Last Updated</div>
                <div class="metric-value" id="last-updated">--:--:--</div>
                <div class="metric-change neutral pulse">Auto-refreshing</div>
            </div>
        </div>
        
        <div class="plugin-section">
            <div class="plugin-title">🔌 Advanced Jenkins Plugins</div>
            <div class="plugin-grid">
                <div class="plugin-card">
                    <div class="plugin-name">🌊 Blue Ocean</div>
                    <div class="plugin-desc">Modern, intuitive pipeline visualization with drag-and-drop pipeline editor and real-time pipeline status.</div>
                </div>
                
                <div class="plugin-card">
                    <div class="plugin-name">📊 Pipeline Stage View</div>
                    <div class="plugin-desc">Visual pipeline stage tracking with detailed stage information and parallel execution visualization.</div>
                </div>
                
                <div class="plugin-card">
                    <div class="plugin-name">🔗 Build Pipeline Plugin</div>
                    <div class="plugin-desc">Dependency management and pipeline visualization with upstream/downstream build relationships.</div>
                </div>
                
                <div class="plugin-card">
                    <div class="plugin-name">📈 Build Time Trend</div>
                    <div class="plugin-desc">Historical build time analysis with trend charts and performance optimization insights.</div>
                </div>
                
                <div class="plugin-card">
                    <div class="plugin-name">🔔 Slack Notification</div>
                    <div class="plugin-desc">Rich Slack notifications with build status, artifacts, and custom formatting for team communication.</div>
                </div>
                
                <div class="plugin-card">
                    <div class="plugin-name">🛡️ Security Plugin</div>
                    <div class="plugin-desc">Security scanning and vulnerability assessment with compliance reporting and risk management.</div>
                </div>
            </div>
        </div>
        
        <div class="comparison-section">
            <div class="comparison-title">Jenkins Configuration Comparison</div>
            <div class="comparison-grid">
                <div class="comparison-item basic-jenkins">
                    <div class="jenkins-title">❌ Basic Jenkins</div>
                    <ul class="jenkins-features">
                        <li>5 basic plugins</li>
                        <li>Simple pipeline syntax</li>
                        <li>Basic notifications</li>
                        <li>Limited visualization</li>
                        <li>Manual configuration</li>
                        <li>No advanced features</li>
                    </ul>
                </div>
                
                <div class="comparison-item powerhouse-jenkins">
                    <div class="jenkins-title">✅ Powerhouse Jenkins</div>
                    <ul class="jenkins-features">
                        <li>25+ advanced plugins</li>
                        <li>Advanced pipeline syntax</li>
                        <li>Rich notifications</li>
                        <li>Visual dashboards</li>
                        <li>Automated configuration</li>
                        <li>Full feature ecosystem</li>
                    </ul>
                </div>
            </div>
        </div>
        
        <div class="auto-refresh">
            🔄 Auto-refresh: 3s
        </div>
    </div>
</body>
</html>
"""

# Global metrics data
metrics_data = {{
    'total_builds': 0,
    'success_rate': 0,
    'avg_duration': 0,
    'plugins_enabled': 0,
    'pipeline_efficiency': 0,
    'user_satisfaction': 0
}}

def update_metrics():
    """Update metrics data periodically."""
    global metrics_data
    while True:
        time.sleep(3)
        metrics_data.update({{
            'total_builds': random.randint(120, 150),
            'success_rate': random.randint(92, 98),
            'avg_duration': random.randint(180, 240),
            'plugins_enabled': random.randint(25, 30),
            'pipeline_efficiency': random.randint(85, 95),
            'user_satisfaction': random.randint(90, 98)
        }})

@app.route('/')
def dashboard():
    """Serve the main dashboard."""
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/metrics')
def api_metrics():
    """API endpoint for metrics data."""
    return jsonify(metrics_data)

if __name__ == '__main__':
    # Start metrics update thread
    metrics_thread = threading.Thread(target=update_metrics, daemon=True)
    metrics_thread.start()
    
    print(f"🚀 Jenkins Powerhouse Dashboard starting on port {port}")
    print(f"📊 Dashboard: http://localhost:{port}")
    print("🔄 Auto-refreshing metrics every 3 seconds")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_basic_jenkins_app(self, port):
        """Create the basic Jenkins limitations app."""
        return f'''#!/usr/bin/env python3
"""
Basic Jenkins Limitations Demo
=============================
Shows the limitations of basic Jenkins setups.
"""

from flask import Flask, render_template_string
import time

app = Flask(__name__)

BASIC_JENKINS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Basic Jenkins Limitations</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .header {{
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .limitations {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .limitation-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #ff4757;
        }}
        .limitation-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .limitation-desc {{
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .warning {{
            background: rgba(255, 193, 7, 0.2);
            border: 2px solid #ffc107;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .warning-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #ffc107;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>❌ Basic Jenkins Limitations</h1>
            <p>Why basic Jenkins setups are insufficient for modern CI/CD</p>
        </div>
        
        <div class="warning">
            <div class="warning-title">⚠️ Basic Jenkins Problems</div>
            <p>Basic Jenkins installations are limited, outdated, and don't leverage 
            the full power of the Jenkins ecosystem. They miss critical features 
            that modern CI/CD requires.</p>
        </div>
        
        <div class="limitations">
            <div class="limitation-item">
                <div class="limitation-title">🔌 Limited Plugins</div>
                <div class="limitation-desc">
                    Basic Jenkins comes with only 5 essential plugins. Missing critical 
                    plugins like Blue Ocean, Pipeline Stage View, and advanced notification 
                    systems that modern teams need.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">📊 Poor Visualization</div>
                <div class="limitation-desc">
                    Basic Jenkins has limited visualization capabilities. No modern 
                    pipeline views, no real-time dashboards, and no advanced reporting 
                    features that help teams understand build performance.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">🔔 Basic Notifications</div>
                <div class="limitation-desc">
                    Only basic email notifications. No Slack integration, no rich 
                    formatting, no conditional notifications, and no team collaboration 
                    features that modern workflows require.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">⚙️ Manual Configuration</div>
                <div class="limitation-desc">
                    Everything requires manual configuration. No automation, no 
                    infrastructure as code, no self-healing capabilities, and no 
                    advanced pipeline optimization features.
                </div>
            </div>
            
            <div class="limitation-item">
                <div class="limitation-title">📈 No Analytics</div>
                <div class="limitation-desc">
                    No build analytics, no performance metrics, no trend analysis, 
                    and no insights into CI/CD efficiency. Teams can't optimize 
                    their processes without data.
                </div>
            </div>
        </div>
        
        <div class="warning">
            <div class="warning-title">💡 The Solution</div>
            <p>Jenkins Powerhouse setup solves all these problems with advanced plugins, 
            modern visualization, rich notifications, automated configuration, and 
            comprehensive analytics. See the next app for the solution!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def basic_jenkins():
    """Serve the basic Jenkins limitations page."""
    return render_template_string(BASIC_JENKINS_TEMPLATE)

if __name__ == '__main__':
    print(f"❌ Basic Jenkins Limitations Demo starting on port {port}")
    print(f"🌐 App: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_powerhouse_jenkins_app(self, port):
        """Create the powerhouse Jenkins benefits app."""
        return f'''#!/usr/bin/env python3
"""
Powerhouse Jenkins Benefits Demo
================================
Shows the benefits and power of advanced Jenkins setups.
"""

from flask import Flask, render_template_string
import time

app = Flask(__name__)

POWERHOUSE_JENKINS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Powerhouse Jenkins Benefits</title>
    <meta charset="utf-8">
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            min-height: 100vh;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            text-align: center;
        }}
        .header {{
            margin-bottom: 40px;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        .benefits {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 30px;
            margin: 20px 0;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }}
        .benefit-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            padding: 20px;
            margin: 15px 0;
            border-left: 5px solid #4CAF50;
        }}
        .benefit-title {{
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 10px;
            color: #ffd700;
        }}
        .benefit-desc {{
            font-size: 1.1em;
            line-height: 1.6;
        }}
        .success {{
            background: rgba(76, 175, 80, 0.2);
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
        }}
        .success-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #4CAF50;
            margin-bottom: 10px;
        }}
        .feature-example {{
            background: rgba(0, 0, 0, 0.2);
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-family: 'Courier New', monospace;
            text-align: left;
        }}
        .feature-example h3 {{
            color: #ffd700;
            margin-top: 0;
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
        }}
        .feature-list li {{
            padding: 8px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }}
        .feature-list li:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>✅ Powerhouse Jenkins Benefits</h1>
            <p>The power and capabilities of advanced Jenkins setups</p>
        </div>
        
        <div class="success">
            <div class="success-title">🎉 Powerhouse Jenkins Advantages</div>
            <p>Powerhouse Jenkins transforms your CI/CD pipeline into a modern, 
            efficient, and feature-rich system that adapts to any requirement 
            and provides maximum productivity.</p>
        </div>
        
        <div class="benefits">
            <div class="benefit-item">
                <div class="benefit-title">🔌 Advanced Plugin Ecosystem</div>
                <div class="benefit-desc">
                    25+ carefully selected plugins including Blue Ocean, Pipeline Stage View, 
                    Build Pipeline Plugin, Slack notifications, security scanning, and 
                    performance analytics. Complete feature coverage for modern CI/CD.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">📊 Rich Visualization & Dashboards</div>
                <div class="benefit-desc">
                    Modern pipeline visualization with Blue Ocean, real-time dashboards, 
                    build trend analysis, performance metrics, and comprehensive reporting. 
                    Teams can see exactly what's happening and optimize accordingly.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">🔔 Advanced Notifications</div>
                <div class="benefit-desc">
                    Rich Slack/Teams notifications, conditional alerts, custom formatting, 
                    artifact sharing, and team collaboration features. Keep everyone 
                    informed with the right information at the right time.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">⚙️ Automated Configuration</div>
                <div class="benefit-desc">
                    Infrastructure as code, automated plugin management, self-healing 
                    capabilities, and advanced pipeline optimization. Minimal manual 
                    intervention with maximum reliability and performance.
                </div>
            </div>
            
            <div class="benefit-item">
                <div class="benefit-title">📈 Comprehensive Analytics</div>
                <div class="benefit-desc">
                    Build performance analytics, trend analysis, efficiency metrics, 
                    bottleneck identification, and optimization recommendations. 
                    Data-driven CI/CD optimization for maximum productivity.
                </div>
            </div>
        </div>
        
        <div class="feature-example">
            <h3>🚀 Powerhouse Features</h3>
            <ul class="feature-list">
                <li><strong>Blue Ocean:</strong> Modern pipeline visualization and editing</li>
                <li><strong>Pipeline Stage View:</strong> Detailed stage tracking and monitoring</li>
                <li><strong>Build Pipeline Plugin:</strong> Dependency management and visualization</li>
                <li><strong>Slack Integration:</strong> Rich team notifications and collaboration</li>
                <li><strong>Security Scanning:</strong> Automated vulnerability assessment</li>
                <li><strong>Performance Analytics:</strong> Build time trends and optimization</li>
                <li><strong>Multi-branch Pipelines:</strong> Automatic branch management</li>
                <li><strong>Parallel Execution:</strong> Optimized build performance</li>
            </ul>
        </div>
        
        <div class="success">
            <div class="success-title">🚀 The Result</div>
            <p>A modern, efficient, and feature-rich Jenkins setup that provides 
            maximum productivity, excellent user experience, and comprehensive 
            CI/CD capabilities. This is the power of Jenkins Powerhouse!</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def powerhouse_jenkins():
    """Serve the powerhouse Jenkins benefits page."""
    return render_template_string(POWERHOUSE_JENKINS_TEMPLATE)

if __name__ == '__main__':
    print(f"✅ Powerhouse Jenkins Benefits Demo starting on port {port}")
    print(f"🌐 App: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def create_basic_app(self, app_name, port):
        """Create a basic demo app."""
        return f'''#!/usr/bin/env python3
"""
{app_name} Demo
==============
Basic demo application.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return f"<h1>{app_name}</h1><p>Demo application running on port {port}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port={port}, debug=False)
'''
    
    def signal_handler(self, signum, frame):
        """Handle interrupt signals."""
        self.print_warning("\\n🛑 Demo interrupted by user")
        self.cleanup()
        sys.exit(0)
    
    def cleanup(self):
        """Clean up running processes."""
        self.print_step("Cleaning up processes...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        self.print_success("Cleanup complete")
    
    def run_demo(self):
        """Run the interactive demo."""
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.print_header("Jenkins Powerhouse - Interactive Demo")
        self.print_info("This demo showcases the power of advanced Jenkins vs basic setups")
        self.print_info("You'll see 3 web applications demonstrating the concepts")
        
        # Install dependencies
        self.print_step("Installing dependencies...")
        if not self.run_command("pip install flask requests pyyaml matplotlib", "Installing Python packages"):
            self.print_error("Failed to install dependencies")
            return False
        
        # Start applications
        apps = [
            ("Jenkins Powerhouse Dashboard", 8000, "Real-time analytics and advanced features"),
            ("Basic Jenkins Limitations", 8001, "Shows basic Jenkins problems"),
            ("Powerhouse Benefits", 8002, "Demonstrates advanced Jenkins power")
        ]
        
        for app_name, port, description in apps:
            if not self.start_application(app_name, port, description):
                self.print_error(f"Failed to start {app_name}")
                return False
            time.sleep(2)  # Give each app time to start
        
        # Open browsers
        self.print_step("Opening web applications...")
        try:
            webbrowser.open('http://localhost:8000')
            time.sleep(1)
            webbrowser.open('http://localhost:8001')
            time.sleep(1)
            webbrowser.open('http://localhost:8002')
        except:
            self.print_warning("Could not auto-open browsers")
        
        # Display URLs
        self.print_success("🎉 Demo applications are running!")
        self.print_info("📊 Dashboard: http://localhost:8000")
        self.print_info("❌ Basic Limitations: http://localhost:8001")
        self.print_info("✅ Powerhouse Benefits: http://localhost:8002")
        self.print_info("")
        self.print_info("Press Ctrl+C to stop the demo")
        
        # Keep running
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

def main():
    """Main function."""
    demo = JenkinsPowerhouseDemo()
    demo.run_demo()

if __name__ == '__main__':
    main()
