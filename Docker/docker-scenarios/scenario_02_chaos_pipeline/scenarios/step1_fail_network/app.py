#!/usr/bin/env python3
import requests
import socket
import subprocess
import time
import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    # Test network connectivity
    network_tests = {
        "dns_resolution": test_dns_resolution(),
        "http_connectivity": test_http_connectivity(),
        "internal_services": test_internal_services()
    }
    
    # Determine overall health based on network tests
    overall_health = any(network_tests.values())
    
    return jsonify({
        "status": "healthy" if overall_health else "unhealthy",
        "step": "step1_fail_network",
        "message": "Network connectivity test",
        "network_tests": network_tests,
        "overall_health": overall_health
    })

@app.route('/debug')
def debug():
    return jsonify({
        "step": "step1_fail_network",
        "description": "Network Failure Simulation",
        "network_info": {
            "hostname": socket.gethostname(),
            "ip_address": get_local_ip(),
            "dns_servers": get_dns_servers(),
            "network_interfaces": get_network_interfaces()
        },
        "connectivity_tests": {
            "dns_resolution": test_dns_resolution(),
            "http_connectivity": test_http_connectivity(),
            "internal_services": test_internal_services()
        },
        "educational_content": {
            "learning_objective": "Understanding container networking limitations",
            "failure_mode": "Network connectivity issues prevent external service access",
            "real_world_impact": "Services cannot reach external APIs, databases, or other services",
            "debugging_tips": [
                "Check DNS resolution",
                "Verify network connectivity",
                "Test service endpoints",
                "Review container network configuration"
            ]
        }
    })

@app.route('/run-experiment')
def run_experiment():
    """Run network connectivity experiment"""
    results = {
        "experiment": "Network Connectivity Test",
        "timestamp": time.time(),
        "tests": {
            "dns_test": test_dns_resolution(),
            "http_test": test_http_connectivity(),
            "internal_test": test_internal_services()
        },
        "summary": "Network connectivity experiment completed",
        "educational_value": "Demonstrates how containers handle network failures"
    }
    
    return jsonify(results)

@app.route('/')
def index():
    return jsonify({
        "message": "Step 1: Network Failure",
        "description": "Network connectivity testing service",
        "endpoints": {
            "health": "/health",
            "debug": "/debug", 
            "experiment": "/run-experiment"
        }
    })

def test_dns_resolution():
    """Test DNS resolution"""
    try:
        socket.gethostbyname("google.com")
        return True
    except:
        return False

def test_http_connectivity():
    """Test HTTP connectivity"""
    try:
        response = requests.get("http://httpbin.org/get", timeout=5)
        return response.status_code == 200
    except:
        return False

def test_internal_services():
    """Test internal service connectivity"""
    try:
        # Try to connect to internal services that don't exist
        socket.create_connection(("internal-service", 8080), timeout=2)
        return True
    except:
        return False

def get_local_ip():
    """Get local IP address"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    s.close()
        return ip
    except:
        return "unknown"

def get_dns_servers():
    """Get DNS servers"""
    try:
        with open("/etc/resolv.conf", "r") as f:
            lines = f.readlines()
            return [line.split()[1] for line in lines if line.startswith("nameserver")]
    except:
        return []

def get_network_interfaces():
    """Get network interfaces"""
    try:
        result = subprocess.run(["ip", "addr", "show"], capture_output=True, text=True)
        return result.stdout
    except:
        return "Unable to get network interfaces"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
