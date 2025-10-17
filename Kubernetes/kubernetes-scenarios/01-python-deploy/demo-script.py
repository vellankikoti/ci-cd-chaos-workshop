#!/usr/bin/env python3
"""
🎭 Universal Chaos Demo Script
Cross-platform demo of manual deployment chaos that works everywhere!

This is the main demo script for Kubernetes scenario 1.
For other scenarios, see their respective demo.py files.
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def run_command(cmd, capture_output=True, check=False):
    """Run a command with proper error handling"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.returncode == 0, result.stdout, result.stderr
        else:
            result = subprocess.run(cmd, shell=True, check=check)
            return True, "", ""
    except subprocess.CalledProcessError as e:
        return False, "", str(e)
    except Exception as e:
        return False, "", str(e)

def print_header(message):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🎭 {message}")
    print("="*60)

def print_step(step, message):
    """Print a step with formatting"""
    print(f"\n📝 Step {step}: {message}")

def print_error(message):
    """Print an error message"""
    print(f"❌ {message}")

def print_success(message):
    """Print a success message"""
    print(f"✅ {message}")

def check_kubernetes_available():
    """Check if kubectl is available"""
    success, _, _ = run_command("kubectl version --client")
    if not success:
        print_error("kubectl not found! Please install kubectl first.")
        print("Install instructions: https://kubernetes.io/docs/tasks/tools/install-kubectl/")
        return False

    # Check if cluster is accessible
    success, _, _ = run_command("kubectl cluster-info")
    if not success:
        print_error("Cannot connect to Kubernetes cluster!")
        print("Please ensure you have a running Kubernetes cluster and proper kubeconfig.")
        return False

    return True

def main():
    """Main demo script"""
    print_header("CHAOS AGENT ATTACK: Manual deployment chaos!")
    print("Watch how 'simple' kubectl commands can fail...")

    # Check prerequisites
    if not check_kubernetes_available():
        sys.exit(1)

    script_dir = Path(__file__).parent
    chaos_dir = script_dir / "chaos"
    broken_manifest = chaos_dir / "broken-vote-app.yaml"

    if not broken_manifest.exists():
        print_error(f"Broken manifest not found: {broken_manifest}")
        print(f"Expected location: {broken_manifest.absolute()}")
        sys.exit(1)

    # Attempt 1: Missing namespace
    print_step(1, "Deploying vote app manually...")
    success, stdout, stderr = run_command(f"kubectl apply -f {broken_manifest}")
    if not success:
        print_error("Failed! Missing namespace...")
        print(f"Error: {stderr}")
    else:
        print_error("Unexpected success - manifest should have failed!")

    time.sleep(2)

    # Attempt 2: Wrong ConfigMap reference
    print_step(2, "Fixing namespace, trying again...")

    # Create namespace
    success, _, _ = run_command("kubectl create namespace vote-app")
    if success:
        print_success("Namespace created")
    else:
        print("⚠️ Namespace might already exist")

    success, stdout, stderr = run_command(f"kubectl apply -f {broken_manifest}")
    if not success:
        print_error("Failed! Missing ConfigMap...")
        print(f"Error: {stderr}")
    else:
        print_error("Unexpected success - should have failed on ConfigMap!")

    time.sleep(2)

    # Attempt 3: Wrong service configuration
    print_step(3, "Creating ConfigMap manually...")

    success, _, _ = run_command('kubectl create configmap vote-config --from-literal=poll_question="Favorite Language?" -n vote-app')
    if success:
        print_success("ConfigMap created")
    else:
        print("⚠️ ConfigMap might already exist")

    success, stdout, stderr = run_command(f"kubectl apply -f {broken_manifest}")
    if not success:
        print_error("Failed! Service misconfiguration...")
        print(f"Error: {stderr}")
    else:
        print_error("Unexpected success - should have failed on Service!")

    time.sleep(2)

    print_header("CHAOS DEMONSTRATION COMPLETE")
    print("😈 Chaos Agent: 'See? Manual deployments are chaos!'")
    print("\n🦸‍♂️ But fear not! The Python Hero has a solution...")
    print("Run the hero solution: python3 hero-solution/deploy.py")

    # Cleanup
    print("\n🧹 Cleaning up demo resources...")
    run_command("kubectl delete namespace vote-app --ignore-not-found=true")
    print_success("Demo cleanup completed!")

if __name__ == "__main__":
    main()