#!/usr/bin/env python3
"""
🧨 CHAOS DEPLOYMENT DEMO - Scenario 01
"When Manual YAML Goes Wrong: A Kubernetes Horror Story"

This script demonstrates what happens when you deploy Kubernetes resources manually
without automation, validation, or proper error handling.
"""

import os
import sys
import time
import subprocess
from pathlib import Path

class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    MAGENTA = '\033[0;35m'
    CYAN = '\033[0;36m'
    BOLD = '\033[1m'
    NC = '\033[0m'  # No Color

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.MAGENTA}{'='*70}{Colors.NC}")
    print(f"{Colors.MAGENTA}{Colors.BOLD}{text}{Colors.NC}")
    print(f"{Colors.MAGENTA}{'='*70}{Colors.NC}\n")

def print_step(text):
    """Print a step"""
    print(f"{Colors.CYAN}▶ {text}{Colors.NC}")

def print_success(text):
    """Print a success message"""
    print(f"{Colors.GREEN}✅ {text}{Colors.NC}")

def print_error(text):
    """Print an error message"""
    print(f"{Colors.RED}❌ {text}{Colors.NC}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.NC}")

def run_command(cmd, description=None, check=False):
    """Run a command and return result"""
    if description:
        print_step(description)

    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            check=check
        )
        return result
    except subprocess.CalledProcessError as e:
        return e

def main():
    """Main chaos demo"""

    print_header("🧨 KUBERNETES CHAOS DEMO - Scenario 01")
    print_header("\"What Could Possibly Go Wrong?\"")

    print(f"{Colors.CYAN}🎓 Learning Objectives:{Colors.NC}")
    print(f"   • Experience the pain of manual YAML deployment")
    print(f"   • See common Kubernetes deployment mistakes")
    print(f"   • Understand why automation matters")
    print(f"   • Learn from failures (the fun way!)")

    print(f"\n{Colors.YELLOW}⚠️  WARNING: This deployment will intentionally fail!{Colors.NC}")
    print(f"{Colors.YELLOW}   That's the whole point - we learn from chaos.{Colors.NC}")

    input(f"\n{Colors.BOLD}Press ENTER to unleash the chaos...{Colors.NC}")

    # Get script directory
    script_dir = Path(__file__).parent
    broken_yaml = script_dir / "broken-vote-app.yaml"

    if not broken_yaml.exists():
        print_error(f"Chaos YAML not found: {broken_yaml}")
        sys.exit(1)

    # STEP 1: Show the broken YAML
    print_header("STEP 1: The Broken YAML Configuration")
    print_step("📄 Let's look at what we're deploying...")

    print(f"\n{Colors.YELLOW}Here's the problematic YAML (common mistakes highlighted):{Colors.NC}\n")
    with open(broken_yaml, 'r') as f:
        for i, line in enumerate(f, 1):
            if 'Missing' in line or 'Wrong' in line or 'Invalid' in line:
                print(f"{Colors.RED}{i:3d} | {line.rstrip()}{Colors.NC}")
            else:
                print(f"{Colors.BLUE}{i:3d} | {line.rstrip()}{Colors.NC}")

    input(f"\n{Colors.BOLD}Press ENTER to attempt deployment (this will fail!)...{Colors.NC}")

    # STEP 2: Try to deploy the broken YAML
    print_header("STEP 2: Deploying the Chaos... 💥")

    print_step("Attempting kubectl apply...")
    result = run_command(
        f"kubectl apply -f {broken_yaml}",
        check=False
    )

    if result.returncode != 0:
        print_error("Deployment failed! (As expected)")
        print(f"\n{Colors.RED}Error Output:{Colors.NC}")
        print(result.stderr)
    else:
        print_warning("Deployment partially succeeded, but things are broken...")

    time.sleep(2)

    # STEP 3: Show the chaos
    print_header("STEP 3: The Aftermath - What Went Wrong?")

    print_step("Checking pod status...")
    pod_result = run_command("kubectl get pods --all-namespaces | grep vote", check=False)

    if pod_result.stdout:
        print(f"\n{Colors.YELLOW}Pod Status:{Colors.NC}")
        print(pod_result.stdout)
    else:
        print_error("No pods found! They didn't even get created.")

    print_step("\nChecking service status...")
    svc_result = run_command("kubectl get svc --all-namespaces | grep vote", check=False)

    if svc_result.stdout:
        print(f"\n{Colors.YELLOW}Service Status:{Colors.NC}")
        print(svc_result.stdout)
    else:
        print_error("No services found!")

    # STEP 4: Educational breakdown
    print_header("STEP 4: What We Learned (The Hard Way)")

    print(f"{Colors.RED}🎯 Problems We Encountered:{Colors.NC}\n")

    problems = [
        ("Missing Namespace", "Resources scattered in default namespace or not created"),
        ("Wrong ConfigMap Reference", "Environment variables fail to inject"),
        ("Invalid NodePort Range", "Service creation fails (valid range: 30000-32767)"),
        ("Wrong Label Selector", "Service can't find pods (selector mismatch)"),
        ("Missing Resource Limits", "No protection against resource exhaustion"),
        ("Missing Health Checks", "No way to know if app is actually working"),
    ]

    for i, (problem, consequence) in enumerate(problems, 1):
        print(f"   {i}. {Colors.YELLOW}{problem}{Colors.NC}")
        print(f"      → {consequence}\n")

    print(f"\n{Colors.CYAN}�� The Manual YAML Nightmare:{Colors.NC}")
    print(f"   • 6+ separate mistakes in just 51 lines of YAML")
    print(f"   • No validation before deployment")
    print(f"   • Cryptic error messages")
    print(f"   • Hours of debugging ahead")
    print(f"   • Different errors in different environments")

    # STEP 5: The solution teaser
    print_header("STEP 5: There's a Better Way... 🦸")

    print(f"{Colors.GREEN}What if instead of manual YAML, you could:{Colors.NC}\n")
    print(f"   ✅ Deploy with {Colors.BOLD}ONE Python command{Colors.NC}")
    print(f"   ✅ Automatic validation before deployment")
    print(f"   ✅ Self-healing with built-in error handling")
    print(f"   ✅ Cross-platform compatibility (Mac, Linux, Windows, Codespaces)")
    print(f"   ✅ Port conflict detection and resolution")
    print(f"   ✅ Interactive web app for testing")
    print(f"   ✅ Clear success/failure indicators")

    print(f"\n{Colors.MAGENTA}That's what the Hero Solution does!{Colors.NC}")

    # Cleanup option
    print_header("Cleanup")

    cleanup = input(f"\n{Colors.YELLOW}Clean up the chaos? (y/n): {Colors.NC}").lower()

    if cleanup == 'y':
        print_step("Cleaning up broken resources...")
        run_command("kubectl delete -f {} --ignore-not-found=true".format(broken_yaml))
        run_command("kubectl delete namespace vote-app --ignore-not-found=true")
        print_success("Chaos cleaned up!")
    else:
        print_warning("Chaos resources left running. Clean up manually with:")
        print(f"   kubectl delete -f {broken_yaml}")
        print(f"   kubectl delete namespace vote-app")

    print_header("🎓 Chaos Demo Complete!")

    print(f"\n{Colors.GREEN}Next Steps:{Colors.NC}")
    print(f"   1. Run the hero solution: {Colors.BOLD}python3 hero-solution/deploy.py{Colors.NC}")
    print(f"   2. Compare: chaos vs automation")
    print(f"   3. Test the working vote app")
    print(f"   4. Never write manual YAML again! 🎉")

    print(f"\n{Colors.CYAN}Remember: Chaos teaches, automation rescues!{Colors.NC}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Chaos demo interrupted!{Colors.NC}")
        print(f"{Colors.CYAN}Run cleanup manually if needed:{Colors.NC}")
        print(f"   kubectl delete namespace vote-app --ignore-not-found=true")
        sys.exit(0)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(1)
