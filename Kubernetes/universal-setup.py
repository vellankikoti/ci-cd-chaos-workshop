#!/usr/bin/env python3
"""
🚀 Universal Kubernetes Workshop Setup Script
Cross-platform setup that works on any environment - local, cloud, or CI/CD!
"""

import subprocess
import sys
import os
import platform
import time
from pathlib import Path

class Colors:
    """ANSI color codes that work cross-platform"""
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def colored_print(message, color=Colors.RESET):
    """Print colored message with fallback for environments without color support"""
    try:
        print(f"{color}{message}{Colors.RESET}")
    except:
        print(message)

def run_command(cmd, capture_output=True, timeout=30):
    """Run command with timeout and error handling"""
    try:
        if capture_output:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
            return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
        else:
            result = subprocess.run(cmd, shell=True, timeout=timeout)
            return result.returncode == 0, "", ""
    except subprocess.TimeoutExpired:
        return False, "", f"Command timed out after {timeout} seconds"
    except Exception as e:
        return False, "", str(e)

def print_header(title):
    """Print formatted header"""
    colored_print("\n" + "="*70, Colors.CYAN)
    colored_print(f"🚀 {title}", Colors.CYAN)
    colored_print("="*70, Colors.CYAN)

def print_step(step, description):
    """Print step information"""
    colored_print(f"\n🔧 Step {step}: {description}", Colors.BLUE)

def print_success(message):
    """Print success message"""
    colored_print(f"✅ {message}", Colors.GREEN)

def print_warning(message):
    """Print warning message"""
    colored_print(f"⚠️ {message}", Colors.YELLOW)

def print_error(message):
    """Print error message"""
    colored_print(f"❌ {message}", Colors.RED)

def detect_environment():
    """Detect the current environment type"""
    colored_print("\n🔍 Detecting environment...", Colors.BLUE)

    env_info = {
        'platform': platform.system(),
        'architecture': platform.machine(),
        'python_version': sys.version,
        'k8s_context': None,
        'k8s_type': 'unknown'
    }

    # Get current Kubernetes context
    success, context, _ = run_command("kubectl config current-context")
    if success:
        env_info['k8s_context'] = context

        # Detect Kubernetes environment type
        if 'docker-desktop' in context.lower():
            env_info['k8s_type'] = 'docker-desktop'
        elif 'minikube' in context.lower():
            env_info['k8s_type'] = 'minikube'
        elif any(cloud in context.lower() for cloud in ['eks', 'gke', 'aks']):
            env_info['k8s_type'] = 'cloud'
        elif 'kind' in context.lower():
            env_info['k8s_type'] = 'kind'
        else:
            env_info['k8s_type'] = 'custom'

    return env_info

def check_prerequisites():
    """Check all prerequisites are met"""
    print_step(1, "Checking prerequisites")

    errors = []
    warnings = []

    # Check Python version
    python_version = sys.version_info
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        errors.append("Python 3.7+ required")
    else:
        print_success(f"Python {python_version.major}.{python_version.minor} ✓")

    # Check required commands
    required_commands = {
        'kubectl': 'Kubernetes CLI',
        'docker': 'Docker CLI',
        'python3': 'Python 3'
    }

    for cmd, description in required_commands.items():
        success, output, _ = run_command(f"{cmd} version")
        if success:
            print_success(f"{description} ✓")
        else:
            if cmd == 'kubectl':
                errors.append(f"{description} not found - required for K8s scenarios")
            else:
                warnings.append(f"{description} not found - some features may not work")

    # Check Kubernetes cluster connectivity
    success, output, error = run_command("kubectl cluster-info")
    if success:
        print_success("Kubernetes cluster accessible ✓")
    else:
        errors.append("Cannot connect to Kubernetes cluster")
        print_error(f"Cluster connection failed: {error}")

    return errors, warnings

def install_python_dependencies():
    """Install required Python packages"""
    print_step(2, "Installing Python dependencies")

    required_packages = [
        'kubernetes',
        'colorama',
        'pyyaml',
        'requests'
    ]

    # Try pip3 first, then pip
    pip_commands = ['pip3', 'pip']
    pip_cmd = None

    for cmd in pip_commands:
        success, _, _ = run_command(f"{cmd} --version")
        if success:
            pip_cmd = cmd
            break

    if not pip_cmd:
        print_error("No pip found! Please install pip manually.")
        return False

    print_success(f"Using {pip_cmd} for package installation")

    # Install packages with fallbacks
    for package in required_packages:
        success, _, error = run_command(f"{pip_cmd} install {package}")
        if success:
            print_success(f"Installed {package}")
        else:
            print_warning(f"Failed to install {package}: {error}")
            # Try with --user flag
            success, _, _ = run_command(f"{pip_cmd} install --user {package}")
            if success:
                print_success(f"Installed {package} (user-level)")
            else:
                print_warning(f"Could not install {package} - some features may not work")

    return True

def setup_workshop_environment():
    """Set up the workshop environment"""
    print_step(3, "Setting up workshop environment")

    # Create workshop namespace
    success, _, _ = run_command("kubectl create namespace chaos-workshop")
    if success:
        print_success("Created chaos-workshop namespace")
    else:
        print_warning("chaos-workshop namespace already exists or creation failed")

    # Set default namespace context (optional)
    success, _, _ = run_command("kubectl config set-context --current --namespace=chaos-workshop")
    if success:
        print_success("Set default namespace to chaos-workshop")

    # Check available resources
    print_success("Checking cluster resources...")
    success, nodes, _ = run_command("kubectl get nodes --no-headers")
    if success:
        node_count = len(nodes.split('\n')) if nodes else 0
        print_success(f"Found {node_count} node(s) in cluster")

    return True

def verify_scenarios():
    """Verify all scenario files exist"""
    print_step(4, "Verifying scenario files")

    script_dir = Path(__file__).parent
    scenarios = [
        "01-python-deploy",
        "02-secret-automation",
        "03-blue-green"
    ]

    missing_scenarios = []

    for scenario in scenarios:
        scenario_dir = script_dir / "kubernetes-scenarios" / scenario
        if scenario_dir.exists():
            print_success(f"Scenario {scenario} ✓")

            # Check for key files (check for .md files instead of README.md)
            md_files = list(scenario_dir.glob("*.md"))
            if md_files:
                print_success(f"  Documentation ({len(md_files)} file(s)) ✓")
            else:
                print_warning(f"  No documentation found")

            # Check for hero-solution directory
            if (scenario_dir / "hero-solution").exists():
                print_success(f"  hero-solution ✓")
            else:
                print_warning(f"  hero-solution missing")
        else:
            missing_scenarios.append(scenario)
            print_error(f"Scenario {scenario} directory missing")

    return len(missing_scenarios) == 0

def provide_next_steps(env_info):
    """Provide environment-specific next steps"""
    print_header("🎯 SETUP COMPLETE - NEXT STEPS")

    colored_print("Your environment is ready! Here's how to proceed:", Colors.GREEN)

    print("\n📚 Available Scenarios:")
    scenarios = [
        ("01-python-deploy", "Deploy Python voting app with automation"),
        ("02-secret-automation", "Secure secret management with automation"),
        ("03-blue-green", "Zero-downtime blue-green deployments")
    ]

    for scenario_id, description in scenarios:
        colored_print(f"  🎭 {scenario_id}: {description}", Colors.CYAN)

    print("\n🚀 Quick Start Commands:")

    if env_info['k8s_type'] == 'minikube':
        colored_print("# Minikube-specific commands:", Colors.YELLOW)
        print("minikube status")
        print("minikube dashboard  # Open K8s dashboard")
    elif env_info['k8s_type'] == 'docker-desktop':
        colored_print("# Docker Desktop commands:", Colors.YELLOW)
        print("docker version")
        print("kubectl get nodes")

    print("\n🎯 Start with scenario 1:")
    print("cd kubernetes-scenarios/01-python-deploy")
    print("python3 demo-script.py  # See the chaos")
    print("python3 hero-solution/deploy-vote-app.py  # Hero saves the day!")

    print("\n📖 For detailed instructions:")
    print("cat kubernetes-scenarios/01-python-deploy/README.md")

def main():
    """Main setup function"""
    print_header("Universal Kubernetes Workshop Setup")
    colored_print("Setting up CI/CD Chaos Workshop for Kubernetes scenarios...", Colors.BLUE)

    # Detect environment
    env_info = detect_environment()
    print(f"\n🌍 Environment: {env_info['platform']} ({env_info['architecture']})")
    print(f"🎯 Kubernetes: {env_info['k8s_type']} - {env_info['k8s_context']}")

    try:
        # Check prerequisites
        errors, warnings = check_prerequisites()

        if errors:
            print_error("Critical errors found:")
            for error in errors:
                print(f"  • {error}")
            print_error("\nPlease fix these errors before continuing.")
            return False

        if warnings:
            print_warning("Warnings (non-critical):")
            for warning in warnings:
                print(f"  • {warning}")

        # Install dependencies
        if not install_python_dependencies():
            print_error("Failed to install Python dependencies")
            return False

        # Setup environment
        if not setup_workshop_environment():
            print_error("Failed to setup workshop environment")
            return False

        # Verify scenarios
        if not verify_scenarios():
            print_warning("Some scenario files are missing - download the complete workshop")

        # Success!
        provide_next_steps(env_info)

        print_header("🎉 SETUP SUCCESSFUL!")
        colored_print("Your Kubernetes workshop environment is ready!", Colors.GREEN)
        colored_print("Have fun defeating the Chaos Agent! 🦸‍♂️", Colors.MAGENTA)

        return True

    except KeyboardInterrupt:
        print_error("\n\nSetup interrupted by user")
        return False
    except Exception as e:
        print_error(f"\nUnexpected error during setup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)