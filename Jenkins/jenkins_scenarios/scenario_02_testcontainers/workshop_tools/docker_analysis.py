#!/usr/bin/env python3

import subprocess
import sys
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table
import datetime

console = Console()

REPORTS_DIR = Path("reports")

def run_cmd(cmd, capture_output=True, shell=False):
    result = subprocess.run(
        cmd,
        check=True,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()

def analyze_docker_image(version_tag):
    image_name = f"ci-cd-chaos-app:v{version_tag}"

    # Get image size
    size_cmd = ["docker", "image", "inspect", image_name, "--format", "{{.Size}}"]
    size_bytes = int(run_cmd(size_cmd))
    size_mb = round(size_bytes / (1024 * 1024), 2)

    console.print(f"📦 Image size for {image_name}: [bold green]{size_mb} MB[/bold green]")

    # Get image history
    history_cmd = ["docker", "history", "--no-trunc", image_name]
    history_output = run_cmd(history_cmd)

    # Save report
    report_dir = REPORTS_DIR / f"version_{version_tag}"
    report_dir.mkdir(parents=True, exist_ok=True)

    report_file = report_dir / "docker_report.html"
    generate_html_report(image_name, size_mb, history_output, report_file)

    console.print(f"✅ Docker report generated for version {version_tag} at [cyan]{report_file}[/cyan]")

def generate_html_report(image_name, size_mb, history_output, report_file):
    # Compose a simple HTML file
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Docker Report for {image_name}</title>
    <style>
        body {{
            font-family: sans-serif;
            margin: 2em;
            background: #111;
            color: #eee;
        }}
        h1 {{
            color: #00ffcc;
        }}
        pre {{
            background: #222;
            padding: 1em;
            border-radius: 8px;
            overflow-x: auto;
        }}
        .stat {{
            color: #0f0;
            font-size: 1.5em;
        }}
    </style>
</head>
<body>
    <h1>Docker Analysis Report</h1>
    <p>Generated on: {now}</p>
    <p><b>Image:</b> {image_name}</p>
    <p><b>Size:</b> <span class="stat">{size_mb} MB</span></p>
    <h2>Image History</h2>
    <pre>{history_output}</pre>
    <h2>Insights</h2>
    <ul>
        <li>✅ Small images deploy faster in CI/CD pipelines.</li>
        <li>✅ Multi-stage builds keep final images tiny.</li>
        <li>✅ Avoid unnecessary layers by combining RUN steps.</li>
        <li>✅ Use specific tags (e.g. python:3.12-slim) for reproducibility.</li>
    </ul>
</body>
</html>
"""
    with open(report_file, "w") as f:
        f.write(html)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]❌ Please provide a Docker image version tag![/red]")
        sys.exit(1)

    version = sys.argv[1]
    analyze_docker_image(version)
