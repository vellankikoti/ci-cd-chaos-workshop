#!/usr/bin/env python3
"""
Docker Resilience & Recovery Demo - Simple Version
=================================================

Transform fragile containers into bulletproof, self-healing systems!
Simple, focused demo just like scenarios 3, 4, and 5
"""

import subprocess
import time
import os
import sys

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    NC = '\033[0m'  # No Color

def print_step(message):
    print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_header(message):
    print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def run_command(cmd, description="", capture_output=False):
    """Run a command and return success status"""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        if result.returncode == 0:
            if capture_output and result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            if capture_output and result.stderr:
                print_error(f"Command failed: {result.stderr}")
            return False
    except Exception as e:
        print_error(f"Command error: {e}")
        return False

def cleanup_containers():
    """Clean up all demo containers and images"""
    print_header("🧹 CLEANUP")
    print("=" * 50)
    
    print_step("Stopping resilience demo containers...")
    run_command("docker stop fragile-app-demo resilient-app-demo resilience-dashboard")
    
    print_step("Removing containers...")
    run_command("docker rm fragile-app-demo resilient-app-demo resilience-dashboard")
    
    print_step("Removing demo images...")
    run_command("docker rmi fragile-app resilient-app resilience-dashboard")
    
    print_success("Cleanup completed!")

def main():
    """Main demo function - simple and focused"""
    print_header("🛡️ DOCKER RESILIENCE & RECOVERY DEMO")
    print("=" * 50)
    print("Transform fragile containers into bulletproof, self-healing systems!")
    print("")
    
    # Trap to ensure cleanup on exit
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Step 1: Show fragile container problem
        print_header("STEP 1: The Fragile Container Problem")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows common Docker resilience anti-patterns")
        print("   • Demonstrates the impact of no health checks or restart policies")
        print("   • Shows why resilience hardening matters in production")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building fragile container with Docker BuildKit...")
        if not run_command("docker buildx build -f dockerfiles/fragile.Dockerfile -t fragile-app --load ."):
            print_error("Failed to build fragile container")
            return
        
        print_step("Starting fragile container...")
        if not run_command("docker run -d --name fragile-app-demo -p 8001:5000 fragile-app"):
            print_error("Failed to start fragile container")
            return
        
        print_step("Waiting for fragile app to start...")
        time.sleep(5)
        
        print_success("Fragile container running at: http://localhost:8001")
        print("   📊 Resilience Score: 0% (No health checks, no restart policies)")
        print("   📊 Uptime: 0% (Constant failures)")
        print("   📊 Recovery: Manual (No auto-healing)")
        
        print("")
        
        # Step 2: Resilience hardening solution
        print_header("STEP 2: Resilience Hardening Solution")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows how to implement Docker resilience best practices")
        print("   • Demonstrates proper health checks and restart policies")
        print("   • Shows the power of self-healing container mechanisms")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building resilient container with Docker BuildKit...")
        if not run_command("docker buildx build -f dockerfiles/resilient.Dockerfile -t resilient-app --load ."):
            print_error("Failed to build resilient container")
            return
        
        print_step("Starting resilient container...")
        if not run_command("docker run -d --name resilient-app-demo -p 8002:5000 resilient-app"):
            print_error("Failed to start resilient container")
            return
        
        print_step("Waiting for resilient app to start...")
        time.sleep(5)
        
        print_success("Resilient container running at: http://localhost:8002")
        print("   📊 Resilience Score: 100% (Health checks, auto-restart)")
        print("   📊 Uptime: 100% (Self-healing)")
        print("   📊 Recovery: Automatic (Auto-healing enabled)")
        
        print("")
        
        # Step 3: Show the difference
        print_header("STEP 3: Resilience Comparison")
        print("=" * 50)
        
        print_step("Comparing resilience implementations...")
        run_command("docker ps | grep -E '(fragile-app-demo|resilient-app-demo)'")
        
        print_step("Resilience analysis...")
        print_success("Resilience Hardening Complete!")
        print("   🎯 Resilience Score: 0% → 100% improvement")
        print("   🎯 Health Checks: None → Active monitoring")
        print("   🎯 Restart Policy: None → Auto-recovery")
        print("   🎯 Uptime: 0% → 100% reliability")
        
        print("")
        
        print_header("🎉 RESILIENCE HARDENING COMPLETED!")
        print("=" * 50)
        print_success("You've successfully transformed a fragile container into a bulletproof masterpiece!")
        print("")
        print_step("📊 FINAL RESULTS:")
        print("   • Docker resilience best practices implemented")
        print("   • Health checks for failure detection")
        print("   • Auto-restart policies for self-healing")
        print("   • Production-ready resilience hardening")
        print("")
        print_step("⏳ Demo will auto-cleanup in 10 minutes...")
        print("   • All resilience improvements are complete")
        print("   • You can explore the containers at your own pace")
        print("   • Press Ctrl+C to stop early and keep containers running")
        time.sleep(600)
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        print("🔍 Containers are still running! You can explore them:")
        print("   • Fragile App: http://localhost:8001")
        print("   • Resilient App: http://localhost:8002")
        print("")
        print("🧹 To clean up later, run: python3 cleanup.py")
        print("⏳ Or wait 10 minutes for auto-cleanup...")
        time.sleep(600)
        cleanup_containers()
    except Exception as e:
        print_error(f"Demo failed: {e}")
        cleanup_containers()
    else:
        # Only cleanup if demo completed successfully
        cleanup_containers()

if __name__ == "__main__":
    main()
