#!/usr/bin/env python3
import psutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import time
import os
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/health')
def health():
    memory_info = get_memory_info()
    return jsonify({
        "status": "healthy" if memory_info["memory_usage_percent"] < 80 else "unhealthy",
        "step": "step2_fail_resource",
        "message": "Resource monitoring service",
        "memory_info": memory_info
    })

@app.route('/debug')
def debug():
    memory_info = get_memory_info()
    return jsonify({
        "step": "step2_fail_resource",
        "description": "Resource Failure Simulation",
        "system_info": {
            "cpu_count": psutil.cpu_count(),
            "cpu_percent": psutil.cpu_percent(),
            "memory_total": memory_info["memory_total_mb"],
            "memory_available": memory_info["memory_available_mb"],
            "memory_used": memory_info["memory_used_mb"],
            "memory_percent": memory_info["memory_usage_percent"]
        },
        "resource_tests": {
            "memory_usage": memory_info["memory_usage_percent"],
            "cpu_usage": psutil.cpu_percent(),
            "disk_usage": psutil.disk_usage('/').percent
        },
        "educational_content": {
            "learning_objective": "Understanding Docker resource management",
            "failure_mode": "Memory exhaustion causes container termination",
            "real_world_impact": "Applications crash when they exceed memory limits",
            "debugging_tips": [
                "Monitor memory usage with psutil",
                "Set appropriate memory limits",
                "Use resource monitoring tools",
                "Implement memory-efficient algorithms"
            ]
        }
    })

@app.route('/run-experiment')
def run_experiment():
    """Run memory-intensive experiment that will likely kill the container"""
    try:
        # Create a very large image that will consume memory
        width, height = 4096, 4096
        image = Image.new('RGB', (width, height), color='red')
        
        # Add some processing to consume more memory
        for i in range(10):
            # Create additional large arrays
            large_array = np.random.rand(1024, 1024)
            processed_array = np.dot(large_array, large_array.T)
            
            # Convert to image and back to consume more memory
            img_array = (processed_array * 255).astype(np.uint8)
            temp_image = Image.fromarray(img_array)
            
        return jsonify({
            "experiment": "Memory Intensive Processing",
            "status": "completed",
            "memory_consumed": "Large amount",
            "result": "Container may be terminated due to OOM",
            "educational_value": "Demonstrates memory limits and OOM killer"
        })
    except MemoryError:
        return jsonify({
            "experiment": "Memory Intensive Processing",
            "status": "failed",
            "error": "MemoryError - Container ran out of memory",
            "educational_value": "Container was killed by OOM killer"
        })
    except Exception as e:
        return jsonify({
            "experiment": "Memory Intensive Processing",
            "status": "error",
            "error": str(e),
            "educational_value": "Unexpected error during memory test"
        })

@app.route('/run-experiment-educational')
def run_experiment_educational():
    """Run educational experiment that won't kill the container"""
    try:
        # Create a smaller image for educational purposes
        width, height = 512, 512
        image = Image.new('RGB', (width, height), color='blue')
        
        # Add some text to the image
        draw = ImageDraw.Draw(image)
        draw.text((50, 50), "Educational Test", fill='white')
        
        # Convert to base64 for display
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            "experiment": "Educational Image Processing",
            "status": "completed",
            "image_size": f"{width}x{height}",
            "memory_usage": get_memory_info()["memory_usage_percent"],
            "image_data": f"data:image/png;base64,{img_str}",
            "educational_value": "Safe image processing demonstration"
        })
    except Exception as e:
        return jsonify({
            "experiment": "Educational Image Processing",
            "status": "error",
            "error": str(e),
            "educational_value": "Error in educational experiment"
        })

@app.route('/run-experiment-safe')
def run_experiment_safe():
    """Run safe experiment with minimal memory usage"""
    try:
        # Create a very small image
        width, height = 64, 64
        image = Image.new('RGB', (width, height), color='green')
        
        # Simple processing
        draw = ImageDraw.Draw(image)
        draw.rectangle([10, 10, 54, 54], fill='yellow')
        
        return jsonify({
            "experiment": "Safe Image Processing",
            "status": "completed",
            "image_size": f"{width}x{height}",
            "memory_usage": get_memory_info()["memory_usage_percent"],
            "educational_value": "Safe processing with minimal memory usage"
        })
    except Exception as e:
        return jsonify({
            "experiment": "Safe Image Processing",
            "status": "error",
            "error": str(e),
            "educational_value": "Error in safe experiment"
        })

@app.route('/process-image/<int:width>/<int:height>')
def process_image(width, height):
    """Process image with specified dimensions"""
    try:
        # Limit dimensions to prevent excessive memory usage
        if width > 1024 or height > 1024:
            return jsonify({
                "error": "Dimensions too large",
                "max_allowed": "1024x1024",
                "requested": f"{width}x{height}"
            }), 400
        
        # Create image
        image = Image.new('RGB', (width, height), color='purple')
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), f"{width}x{height}", fill='white')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        image.save(img_buffer, format='PNG')
        img_str = base64.b64encode(img_buffer.getvalue()).decode()
        
        return jsonify({
            "status": "success",
            "image_size": f"{width}x{height}",
            "memory_usage": get_memory_info()["memory_usage_percent"],
            "image_data": f"data:image/png;base64,{img_str}"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

@app.route('/')
def index():
    return jsonify({
        "message": "Step 2: Resource Failure",
        "description": "Image processing and memory monitoring service",
        "endpoints": {
            "health": "/health",
            "debug": "/debug",
            "experiment": "/run-experiment",
            "educational_experiment": "/run-experiment-educational",
            "safe_experiment": "/run-experiment-safe",
            "process_image": "/process-image/<width>/<height>"
        }
    })

def get_memory_info():
    """Get detailed memory information"""
    memory = psutil.virtual_memory()
    return {
        "memory_total_mb": round(memory.total / (1024 * 1024), 2),
        "memory_available_mb": round(memory.available / (1024 * 1024), 2),
        "memory_used_mb": round(memory.used / (1024 * 1024), 2),
        "memory_usage_percent": round(memory.percent, 2)
    }

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
