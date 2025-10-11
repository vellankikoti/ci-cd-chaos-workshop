#!/usr/bin/env python3
"""
🚀 Blue-Green Deployment Manager
Simple, clean script to demonstrate zero-downtime deployments
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def run_command(cmd, description, check=True):
    """Run a command and print output"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"$ {cmd}\n")

    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)

    if check and result.returncode != 0:
        print(f"\n❌ Failed: {description}")
        return False

    print(f"\n✅ Success: {description}")
    return True

def detect_environment():
    """Detect Kubernetes environment"""
    print("\n🔍 Detecting Kubernetes environment...")
    result = subprocess.run("kubectl config current-context",
                          shell=True, capture_output=True, text=True)
    context = result.stdout.strip()

    if "minikube" in context:
        print("✅ Detected: Minikube")
        return "minikube"
    elif "docker-desktop" in context:
        print("✅ Detected: Docker Desktop")
        return "docker-desktop"
    else:
        print(f"✅ Detected: {context}")
        return "unknown"

def get_current_version():
    """Get currently active version from service"""
    result = subprocess.run(
        "kubectl get service demo-app -n blue-green-demo -o jsonpath='{.spec.selector.version}' 2>/dev/null",
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip() or "none"

def switch_version(target_version):
    """Switch service to target version (blue or green)"""
    print(f"\n🔄 Switching traffic to {target_version.upper()} version...")

    cmd = f"kubectl patch service demo-app -n blue-green-demo -p '{{\"spec\":{{\"selector\":{{\"version\":\"{target_version}\"}}}}}}'"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✅ Traffic switched to {target_version.upper()}")
        return True
    else:
        print(f"❌ Failed to switch traffic")
        return False

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║  🚀 BLUE-GREEN DEPLOYMENT DEMO                            ║
║  Simple, Clean, Zero-Downtime!                             ║
╚════════════════════════════════════════════════════════════╝
""")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    env = detect_environment()

    # Build Docker image
    image_name = "blue-green-demo:latest"

    if env == "minikube":
        print("\n📦 Building image inside Minikube...")
        if not run_command(
            "eval $(minikube docker-env) && docker build -t " + image_name + " .",
            "Build image in Minikube"
        ):
            if not run_command(f"docker build -t {image_name} .", "Build image locally"):
                return False
    else:
        if not run_command(f"docker build -t {image_name} .", "Build Docker image"):
            return False

    # Update manifest
    print("\n📝 Updating Kubernetes manifest...")
    with open('k8s-manifests.yaml', 'r') as f:
        manifest = f.read()

    # Set initial version to blue
    manifest = manifest.replace('YOUR_IMAGE_HERE', image_name)
    manifest = manifest.replace('ACTIVE_VERSION', 'blue')

    with open('k8s-deployed.yaml', 'w') as f:
        f.write(manifest)

    print("✅ Manifest updated")

    # Deploy
    if not run_command("kubectl apply -f k8s-deployed.yaml", "Deploy to Kubernetes"):
        return False

    # Wait for pods
    print("\n⏳ Waiting for pods to be ready...")
    for i in range(30):
        result = subprocess.run(
            "kubectl get pods -n blue-green-demo -o jsonpath='{.items[*].status.phase}'",
            shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            phases = result.stdout.strip().split()
            if phases and all(p == 'Running' for p in phases):
                print("\n✅ All pods are running!")
                break

        print(f"   Attempt {i+1}/30: Waiting...")
        time.sleep(5)

    # Show current state
    current = get_current_version()

    # Show success
    print(f"\n{'='*60}")
    print("🎉 DEPLOYMENT COMPLETE!")
    print(f"{'='*60}\n")

    print(f"🎯 CURRENT VERSION: {current.upper()}\n")

    print("🌐 ACCESS YOUR APP:\n")
    print("   🎯 Try NodePort: http://localhost:31006")
    print("   ℹ️  If that doesn't work, use port-forward below:")

    print("\n🔧 PORT-FORWARD COMMANDS (Copy & Paste):\n")
    print("   # Terminal 1: Start port-forward")
    print("   kubectl port-forward -n blue-green-demo svc/demo-app 31006:80")
    print()
    print("   # Then open: http://localhost:31006")

    print("\n🔄 SWITCH BETWEEN VERSIONS:\n")
    print("   # Switch to GREEN (v2.0)")
    print("   python3 switch.py green")
    print()
    print("   # Switch to BLUE (v1.0)")
    print("   python3 switch.py blue")
    print()
    print("   # Check current version")
    print("   python3 switch.py status")

    print("\n📊 VERIFY DEPLOYMENT:\n")
    print("   kubectl get all -n blue-green-demo")
    print("   kubectl get pods -n blue-green-demo -L version")
    print("   kubectl describe service demo-app -n blue-green-demo")

    print("\n🎮 TRY ZERO-DOWNTIME DEPLOYMENT:\n")
    print("   1. Open http://localhost:31006 in your browser")
    print("   2. Run: python3 switch.py green")
    print("   3. Watch the page auto-refresh to show GREEN version")
    print("   4. Run: python3 switch.py blue")
    print("   5. Watch it switch back to BLUE - zero downtime!")

    print("\n🔐 BLUE-GREEN DEPLOYMENT BENEFITS:\n")
    print("   ✅ Zero downtime deployments")
    print("   ✅ Instant rollback capability")
    print("   ✅ Easy A/B testing")
    print("   ✅ Reduced risk of deployment failures")
    print("   ✅ Both environments identical")

    print("\n🧹 CLEANUP:\n")
    print("   kubectl delete namespace blue-green-demo")
    print("   rm k8s-deployed.yaml")

    print(f"\n{'='*60}")
    print("✅ Ready! Open http://localhost:31006 and try switching!")
    print(f"{'='*60}\n")

    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
