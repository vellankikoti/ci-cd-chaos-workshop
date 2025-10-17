#!/usr/bin/env python3
"""
🚀 Blue-Green Deployment Manager
Automatically detects and deploys enhanced version if available, otherwise standard version
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
    elif "kind" in context:
        print("✅ Detected: Kind")
        return "kind"
    else:
        print(f"✅ Detected: {context}")
        return "unknown"

def detect_version():
    """Always use standard version"""
    return "standard"

def get_current_version():
    """Get currently active version from service"""
    result = subprocess.run(
        "kubectl get service demo-app -n blue-green-demo -o jsonpath='{.spec.selector.version}' 2>/dev/null",
        shell=True, capture_output=True, text=True
    )
    return result.stdout.strip() or "none"

def main():
    # Detect version
    version = detect_version()

    if version == "enhanced":
        print("""
╔════════════════════════════════════════════════════════════╗
║  🚀 BLUE-GREEN DEPLOYMENT - Enhanced Traffic Viz          ║
║  Live Traffic Visualization & Interactive Control Panel!  ║
╚════════════════════════════════════════════════════════════╝
""")
    else:
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
    app_file = "app.py"
    print("\n📦 Building blue-green app...")

    build_cmd = f"docker build --build-arg APP_FILE={app_file} -t {image_name} ."

    if env == "minikube":
        print(f"\n📦 Building image inside Minikube...")
        if not run_command(
            f"eval $(minikube docker-env) && {build_cmd}",
            f"Build {version} image in Minikube"
        ):
            if not run_command(build_cmd, f"Build {version} image locally"):
                return False
    else:
        if not run_command(build_cmd, f"Build {version} Docker image"):
            return False

    # Load into Kind if needed
    if env == "kind":
        print("\n📦 Loading image into Kind cluster...")
        run_command(f"kind load docker-image {image_name}", "Load image into Kind", check=False)

    # Update manifest
    print("\n📝 Updating Kubernetes manifest...")
    with open('k8s-manifests.yaml', 'r') as f:
        manifest = f.read()

    # Set initial version to blue
    manifest = manifest.replace('YOUR_IMAGE_HERE', image_name)
    manifest = manifest.replace('ACTIVE_VERSION', 'blue')

    with open('k8s-deployed.yaml', 'w') as f:
        f.write(manifest)

    print(f"✅ Manifest updated for {version} version")

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

    if version == "enhanced":
        print("🌟 ENHANCED VERSION DEPLOYED!")
        print("   Live Traffic Visualization Dashboard!\n")

    print(f"🎯 CURRENT VERSION: {current.upper()}\n")

    print("🌐 ACCESS YOUR APP:\n")
    print("   🎯 Try NodePort: http://localhost:31006")
    print("   ℹ️  If that doesn't work, use port-forward below:")

    print("\n🔧 PORT-FORWARD COMMAND (Copy & Paste):\n")
    print("   kubectl port-forward -n blue-green-demo svc/demo-app 31006:80")
    print()
    print("   # Then open: http://localhost:31006")

    if version == "enhanced":
        print("\n✨ ENHANCED FEATURES AVAILABLE:")
        print("   🌊 Animated traffic particles flowing from load balancer to pods")
        print("   🎛️  Interactive traffic slider (0-100% control)")
        print("   📊 Live pod health with heartbeat animations")
        print("   🚀 One-click 'Switch to Green' button")
        print("   ↩️  One-click 'Rollback to Blue' button")
        print("   📈 Real-time metrics dashboard")
        print("   📜 Live request history")

    print("\n🔄 SWITCH BETWEEN VERSIONS:\n")
    print("   # Switch to GREEN (v2.0)")
    print("   python3 switch.py green")
    print()
    print("   # Switch to BLUE (v1.0)")
    print("   python3 switch.py blue")
    print()
    print("   # Check current version")
    print("   python3 switch.py status")

    if version == "enhanced":
        print("\n💡 TIP: Use the web dashboard to switch - it's interactive!")

    print("\n📊 VERIFY DEPLOYMENT:\n")
    print("   kubectl get all -n blue-green-demo")
    print("   kubectl get pods -n blue-green-demo -L version")
    print("   kubectl describe service demo-app -n blue-green-demo")

    print("\n🔐 BLUE-GREEN DEPLOYMENT BENEFITS:\n")
    print("   ✅ Zero downtime deployments")
    print("   ✅ Instant rollback capability")
    print("   ✅ Easy A/B testing")
    print("   ✅ Reduced risk of deployment failures")
    print("   ✅ Both environments identical")
    if version == "enhanced":
        print("   ✅ Visual confidence - see exactly what's happening!")

    print("\n🧹 CLEANUP:\n")
    print("   kubectl delete namespace blue-green-demo")
    print("   rm k8s-deployed.yaml")

    print(f"\n{'='*60}")
    if version == "enhanced":
        print("✅ Enhanced Traffic Visualization Ready!")
        print("Open http://localhost:31006 for LIVE TRAFFIC FLOW!")
        print("Click buttons to switch traffic - watch it animate! 🌊")
    else:
        print("✅ Blue-Green Demo Ready!")
        print("Open http://localhost:31006 and try switching!")
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
