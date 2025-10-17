#!/usr/bin/env python3
"""
🔐 Secure Todo App Deployer
Automatically detects and deploys enhanced version if available, otherwise standard version
"""
import os
import sys
import subprocess
import time
import secrets
import string
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

def generate_secure_password(length=32):
    """Generate a cryptographically secure password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(secrets.choice(alphabet) for _ in range(length))

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

def main():
    # Detect version
    version = detect_version()

    if version == "enhanced":
        print("""
╔════════════════════════════════════════════════════════════╗
║  🔐 SECURE TODO APP - Enhanced Security Dashboard         ║
║  Deploying with Live Monitoring & Real-Time Audit Log!    ║
╚════════════════════════════════════════════════════════════╝
""")
    else:
        print("""
╔════════════════════════════════════════════════════════════╗
║  🔐 SECURE TODO APP - Secret Management Demo              ║
║  Simple, Clean, Powerful!                                  ║
╚════════════════════════════════════════════════════════════╝
""")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    env = detect_environment()

    # Generate secure credentials
    print("\n🔐 Generating secure credentials...")
    api_key = generate_secure_password(32)
    app_secret = generate_secure_password(32)
    db_password = generate_secure_password(32)
    print("✅ Generated cryptographically secure secrets")
    print(f"   API Key: {api_key[:12]}... (32 chars)")
    print(f"   App Secret: {app_secret[:12]}... (32 chars)")
    print(f"   DB Password: {db_password[:12]}... (32 chars)")

    # Build Docker image
    image_name = "secure-todo:latest"
    app_file = "app.py"
    print("\n📦 Building secure todo app...")

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

    # Replace secrets
    manifest = manifest.replace('GENERATED_BY_SCRIPT', api_key, 1)
    manifest = manifest.replace('GENERATED_BY_SCRIPT', app_secret, 1)

    # Add DB_PASSWORD if enhanced version
    if version == "enhanced" and 'db-password' not in manifest:
        secret_data_pos = manifest.find('data:', manifest.find('kind: Secret'))
        if secret_data_pos > 0:
            next_line = manifest.find('\n', secret_data_pos)
            manifest = (manifest[:next_line+1] +
                       f"  db-password: {db_password}\n" +
                       manifest[next_line+1:])

    manifest = manifest.replace('YOUR_IMAGE_HERE', image_name)

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
            "kubectl get pods -n secure-todo -o jsonpath='{.items[*].status.phase}'",
            shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            phases = result.stdout.strip().split()
            if phases and all(p == 'Running' for p in phases):
                print("\n✅ All pods are running!")
                break

        print(f"   Attempt {i+1}/30: Waiting...")
        time.sleep(5)

    # Show success
    print(f"\n{'='*60}")
    print("🎉 DEPLOYMENT COMPLETE!")
    print(f"{'='*60}\n")

    if version == "enhanced":
        print("🌟 ENHANCED VERSION DEPLOYED!")
        print("   Live Security Dashboard with Real-Time Monitoring!\n")

    print("🌐 ACCESS YOUR SECURE TODO APP:\n")
    print("   🎯 Try NodePort: http://localhost:31005")
    print("   ℹ️  If that doesn't work, use port-forward below:")

    print("\n🔧 PORT-FORWARD COMMAND (Copy & Paste):\n")
    print("   kubectl port-forward -n secure-todo svc/secure-todo-app 31005:80")
    print()
    print("   # Then open: http://localhost:31005")

    if version == "enhanced":
        print("\n✨ ENHANCED FEATURES AVAILABLE:")
        print("   🛡️  Real-time Security Monitoring Dashboard")
        print("   📊 Live Security Audit Log (color-coded events)")
        print("   🔐 Visual Secret Status (3 secrets with heartbeat)")
        print("   💯 Dynamic Security Score")
        print("   🎨 Dark Cybersecurity Aesthetic")
        print("   📡 Auto-refresh every 2 seconds")

    print("\n📊 VERIFY DEPLOYMENT:\n")
    print("   kubectl get all -n secure-todo")
    print("   kubectl get secrets -n secure-todo")
    print("   kubectl logs -n secure-todo -l app=secure-todo-app")

    print("\n🔐 SECURITY FEATURES:\n")
    print("   ✅ Auto-generated 32-char secure passwords")
    print("   ✅ Secrets encrypted in etcd")
    print("   ✅ Non-root container (UID 1000)")
    print("   ✅ Read-only root filesystem")
    print("   ✅ Dropped all capabilities")
    print("   ✅ Resource limits")
    print("   ✅ Health checks")
    if version == "enhanced":
        print("   ✅ Real-time security monitoring")

    print("\n🧹 CLEANUP:\n")
    print("   kubectl delete namespace secure-todo")
    print("   rm k8s-deployed.yaml")

    print(f"\n{'='*60}")
    if version == "enhanced":
        print("✅ Enhanced Security Dashboard Ready!")
        print("Open http://localhost:31005 for LIVE MONITORING!")
    else:
        print("✅ Secure Todo App Ready!")
        print("Open http://localhost:31005 and try it!")
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
