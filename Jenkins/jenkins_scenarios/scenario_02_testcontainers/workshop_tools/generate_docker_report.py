#!/usr/bin/env python3

import docker
import os
import sys
from jinja2 import Environment, FileSystemLoader

# Define the template directory
TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "templates"
)

# Ensure template folder exists
os.makedirs(TEMPLATE_DIR, exist_ok=True)

# Path to the HTML template
TEMPLATE_PATH = os.path.join(TEMPLATE_DIR, "docker_report_template.html")

# Write the updated template if it doesn't exist
if not os.path.exists(TEMPLATE_PATH):
    with open(TEMPLATE_PATH, "w") as f:
        f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>🚀 Docker Report for Version {{ version }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f9fbfe;
            color: #333;
            margin: 0;
            padding: 20px;
        }
        h1 {
            color: #0069d9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        table, th, td {
            border: 1px solid #007bff;
        }
        th {
            background-color: #007bff;
            color: white;
            padding: 8px;
        }
        td {
            padding: 8px;
            word-break: break-all;
        }
        th:nth-child(1), td:nth-child(1) {
            width: 50px;
            text-align: center;
        }
        th:nth-child(2), td:nth-child(2) {
            width: 450px;
        }
        th:nth-child(3), td:nth-child(3) {
            width: 100px;
            text-align: right;
        }
        th:nth-child(4), td:nth-child(4) {
            width: auto;
        }
    </style>
</head>
<body>
    <h1>🚀 Docker Report for Version {{ version }}</h1>

    <p><strong>Image Tag:</strong> {{ image_tag }}</p>
    <p><strong>Size:</strong> {{ image_size }} MB</p>
    <p><strong>Created At:</strong> {{ created_at }}</p>

    <h2>Base Image</h2>
    <p>{{ base_image }}</p>

    <h2>Exposed Ports</h2>
    <ul>
        {% for port in exposed_ports %}
        <li>{{ port }}</li>
        {% else %}
        <li>No ports exposed.</li>
        {% endfor %}
    </ul>

    <h2>Environment Variables</h2>
    <ul>
        {% for env_var in env_vars %}
        <li>{{ env_var }}</li>
        {% else %}
        <li>No environment variables found.</li>
        {% endfor %}
    </ul>

    <h2>Layer Digests (Filesystem Layers)</h2>
    {% if layer_digests %}
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Layer Digest</th>
            </tr>
        </thead>
        <tbody>
        {% for digest in layer_digests %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ digest }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No layer digests found.</p>
    {% endif %}

    <h2>Docker Build History</h2>
    {% if layers %}
    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Instruction</th>
                <th>Size (MB)</th>
            </tr>
        </thead>
        <tbody>
        {% for layer in layers %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ layer.command }}</td>
                <td>{{ layer.size }}</td>
            </tr>
        {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>No build history found.</p>
    {% endif %}

    <h2>💡 Recommendations</h2>
    <ul>
        {% for rec in recommendations %}
            <li>{{ rec }}</li>
        {% else %}
            <li>No recommendations. Looking good! 🎉</li>
        {% endfor %}
    </ul>

</body>
</html>
        """)

# Initialize Jinja environment
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

def generate_report(version):
    client = docker.from_env()

    tag = f"ci-cd-chaos-app:v{version}"
    try:
        image = client.images.get(tag)
    except docker.errors.ImageNotFound:
        print(f"❌ Image {tag} not found.")
        sys.exit(1)

    # General image details
    image_size = round(image.attrs["Size"] / (1024 * 1024), 1)
    created_at = image.attrs["Created"]

    # Exposed ports
    exposed_ports = []
    config_ports = image.attrs["Config"].get("ExposedPorts", {})
    for port in config_ports:
        exposed_ports.append(port)

    # Environment variables
    env_vars = image.attrs["Config"].get("Env", [])

    # Real unique layer digests
    layer_digests = image.attrs.get("RootFS", {}).get("Layers", [])

    # Docker build history
    history = client.api.history(image.id)
    layers = []
    for layer in reversed(history):
        command = layer.get("CreatedBy", "").strip()
        size_mb = round(layer.get("Size", 0) / (1024 * 1024), 1)
        layers.append({
            "command": command,
            "size": size_mb
        })

    # Find the base image (FROM)
    base_image = "Unknown"
    for layer in reversed(history):
        if "FROM" in layer.get("CreatedBy", "").upper():
            base_image = layer.get("CreatedBy")
            break

    # Recommendations
    recommendations = []
    if image_size > 150:
        recommendations.append("Consider using a smaller base image (e.g. python:3.12-slim).")
    if not exposed_ports:
        recommendations.append("Consider exposing a port to run your application.")
    if not env_vars:
        recommendations.append("Consider defining environment variables for your app.")

    # Render HTML
    template = env.get_template("docker_report_template.html")
    html = template.render(
        version=version,
        image_tag=tag,
        image_size=image_size,
        created_at=created_at,
        base_image=base_image,
        exposed_ports=exposed_ports,
        env_vars=env_vars,
        layer_digests=layer_digests,
        layers=layers,
        recommendations=recommendations
    )

    # Save report
    report_dir = f"reports/version_{version}"
    os.makedirs(report_dir, exist_ok=True)
    output_path = os.path.join(report_dir, "docker_report.html")

    with open(output_path, "w") as f:
        f.write(html)

    print(f"✅ Docker report generated for version {version} at {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_docker_report.py <version>")
        sys.exit(1)

    generate_report(sys.argv[1])
