#!/usr/bin/env python3
"""
Docker Multi-Stage Build Interactive Demo
========================================

Demonstrate multi-stage build optimization with interactive components
"""

import subprocess
import time
import os
import sys
import json

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    PURPLE = '\033[0;35m'
    RED = '\033[0;31m'
    CYAN = '\033[0;36m'
    NC = '\033[0m'  # No Color

def print_step(message):
    print(f"{Colors.BLUE}🔹 {message}{Colors.NC}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.NC}")

def print_header(message):
    print(f"{Colors.PURPLE}🎯 {message}{Colors.NC}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.NC}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.NC}")

def print_info(message):
    print(f"{Colors.CYAN}ℹ️ {message}{Colors.NC}")

def run_command(cmd, description="", capture_output=False, show_output=True):
    """Run a command and return success status"""
    if description:
        print_step(description)
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=capture_output, text=True)
        if result.returncode == 0:
            if capture_output and result.stdout and show_output:
                print(f"   Output: {result.stdout.strip()}")
            return True, result.stdout if capture_output else None
        else:
            if capture_output and result.stderr:
                print_error(f"Command failed: {result.stderr}")
            return False, result.stderr if capture_output else None
    except Exception as e:
        print_error(f"Command error: {e}")
        return False, str(e)

def get_image_size(image_name):
    """Get the size of a Docker image"""
    success, output = run_command(f"docker images {image_name} --format '{{{{.Size}}}}'", capture_output=True, show_output=False)
    if success and output:
        return output.strip()
    return "Unknown"

def get_image_layers(image_name):
    """Get the number of layers in a Docker image"""
    success, output = run_command(f"docker history {image_name} --no-trunc | wc -l", capture_output=True, show_output=False)
    if success and output:
        try:
            # Subtract 1 for header line
            return str(int(output.strip()) - 1)
        except:
            return "Unknown"
    return "Unknown"

def cleanup_containers():
    """Clean up all demo containers and images"""
    print_header("🧹 CLEANUP")
    print("=" * 50)
    
    print_step("Stopping containers...")
    run_command("docker stop bloated-app-demo optimized-app-demo comparison-app", show_output=False)
    
    print_step("Removing containers...")
    run_command("docker rm bloated-app-demo optimized-app-demo comparison-app", show_output=False)
    
    print_step("Removing demo images...")
    run_command("docker rmi bloated-app optimized-app comparison-demo", show_output=False)
    
    print_success("Cleanup completed!")

def show_image_comparison():
    """Display a comparison table of the images"""
    print_header("📊 IMAGE COMPARISON")
    print("=" * 80)
    
    bloated_size = get_image_size("bloated-app")
    optimized_size = get_image_size("optimized-app")
    bloated_layers = get_image_layers("bloated-app")
    optimized_layers = get_image_layers("optimized-app")
    
    print(f"{'Image Type':<20} {'Size':<15} {'Layers':<10} {'Status':<15}")
    print("-" * 70)
    print(f"{'Bloated':<20} {bloated_size:<15} {bloated_layers:<10} {'❌ Poor':<15}")
    print(f"{'Optimized':<20} {optimized_size:<15} {optimized_layers:<10} {'✅ Great':<15}")
    print("-" * 70)
    
    # Calculate improvement if both sizes are available
    try:
        if "GB" in bloated_size and "MB" in optimized_size:
            bloated_mb = float(bloated_size.replace("GB", "")) * 1024
            optimized_mb = float(optimized_size.replace("MB", ""))
            reduction = ((bloated_mb - optimized_mb) / bloated_mb) * 100
            print_success(f"Size reduction: {reduction:.1f}% smaller!")
        elif "MB" in bloated_size and "MB" in optimized_size:
            bloated_mb = float(bloated_size.replace("MB", ""))
            optimized_mb = float(optimized_size.replace("MB", ""))
            reduction = ((bloated_mb - optimized_mb) / bloated_mb) * 100
            print_success(f"Size reduction: {reduction:.1f}% smaller!")
    except:
        pass

def main():
    """Main interactive demo function"""
    print_header("🏗️ DOCKER MULTI-STAGE BUILD INTERACTIVE DEMO")
    print("=" * 60)
    print("Transform bloated images into production-ready masterpieces!")
    print()
    
    # Trap to ensure cleanup on exit
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Step 1: Build the bloated image with live feedback
        print_header("STEP 1: Building the Bloated Image")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This demonstrates common Docker anti-patterns")
        print("   • Shows the impact of inefficient builds")
        print("   • Watch how the size grows with unnecessary components")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building bloated image (this may take a while)...")
        print_info("Watch the build process - notice all the unnecessary packages being installed!")
        
        success, _ = run_command("docker buildx build -f dockerfiles/bloated.Dockerfile -t bloated-app --load .")
        if not success:
            print_error("Failed to build bloated image")
            return
        
        bloated_size = get_image_size("bloated-app")
        bloated_layers = get_image_layers("bloated-app")
        
        print_success(f"Bloated image built successfully!")
        print_info(f"   Size: {bloated_size}")
        print_info(f"   Layers: {bloated_layers}")
        
        print_step("Starting bloated app container...")
        success, _ = run_command("docker run -d --name bloated-app-demo -p 8001:5000 bloated-app")
        if not success:
            print_error("Failed to start bloated app")
            return
        
        print_step("Waiting for bloated app to start...")
        time.sleep(5)
        
        print_success("Bloated app running at: http://localhost:8001")
        print_warning(f"Notice the massive size: {bloated_size} - this is problematic for production!")
        
        print()
        
        # Step 2: Build the optimized multi-stage image
        print_header("STEP 2: Building the Optimized Multi-Stage Image")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This demonstrates multi-stage build optimization")
        print("   • Build stage: Contains build tools and dependencies")
        print("   • Production stage: Only runtime dependencies")
        print("   • Watch how much smaller and faster it is!")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building optimized multi-stage image...")
        print_info("Notice the two stages: builder -> production")
        
        success, _ = run_command("docker buildx build -f dockerfiles/optimized.Dockerfile -t optimized-app --load .")
        if not success:
            print_error("Failed to build optimized image")
            return
        
        optimized_size = get_image_size("optimized-app")
        optimized_layers = get_image_layers("optimized-app")
        
        print_success(f"Optimized image built successfully!")
        print_info(f"   Size: {optimized_size}")
        print_info(f"   Layers: {optimized_layers}")
        
        print_step("Starting optimized app container...")
        success, _ = run_command("docker run -d --name optimized-app-demo -p 8002:5000 optimized-app")
        if not success:
            print_error("Failed to start optimized app")
            return
        
        print_step("Waiting for optimized app to start...")
        time.sleep(5)
        
        print_success("Optimized app running at: http://localhost:8002")
        print_success(f"Much better size: {optimized_size} - production ready!")
        
        print()
        
        # Step 3: Create comparison app
        print_header("STEP 3: Interactive Comparison Dashboard")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • Interactive web dashboard showing the comparison")
        print("   • Real-time size metrics and build information")
        print("   • Visual representation of the optimization benefits")
        print("   • Layer analysis and security improvements")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Creating enhanced comparison app...")
        
        # Create the comparison app
        success, _ = run_command("docker buildx build -f app/Dockerfile -t comparison-demo --load app/")
        if not success:
            print_error("Failed to build comparison app")
            return
        
        print_step("Starting interactive comparison dashboard...")
        success, _ = run_command("docker run -d --name comparison-app -p 8000:5000 -v /var/run/docker.sock:/var/run/docker.sock comparison-demo")
        if not success:
            print_error("Failed to start comparison app")
            return
        
        print_step("Waiting for comparison dashboard to start...")
        time.sleep(5)
        
        print()
        
        # Step 4: Show detailed analysis
        print_header("STEP 4: Detailed Analysis & Layer Inspection")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • Deep dive into Docker layers and image composition")
        print("   • Understanding build cache optimization")
        print("   • Security implications of image size")
        print("   • Production deployment considerations")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        # Show detailed comparison
        show_image_comparison()
        
        print()
        print_step("Analyzing Docker layers...")
        print_info("Bloated image layers:")
        run_command("docker history bloated-app --format 'table {{.CreatedBy}}\\t{{.Size}}' | head -10")
        
        print()
        print_info("Optimized image layers:")
        run_command("docker history optimized-app --format 'table {{.CreatedBy}}\\t{{.Size}}' | head -10")
        
        print()
        
        # Step 5: Interactive exploration
        print_header("STEP 5: Interactive Exploration")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • Hands-on exploration of the optimization benefits")
        print("   • Compare startup times, security, and efficiency")
        print("   • Real-world production deployment scenarios")
        
        print_success("🌐 INTERACTIVE APPLICATIONS ARE READY!")
        print("=" * 60)
        print_info("📊 Comparison Dashboard: http://localhost:8000")
        print_info("   • Live metrics and size comparison")
        print_info("   • Layer analysis and optimization tips")
        print_info("   • Interactive build process visualization")
        print()
        print_info("🚀 Bloated App (4.2GB):   http://localhost:8001")
        print_info("   • See what NOT to do in production")
        print_info("   • Notice slower startup and larger attack surface")
        print()
        print_info("✨ Optimized App (267MB): http://localhost:8002")
        print_info("   • Production-ready, secure, and efficient")
        print_info("   • Fast startup and minimal dependencies")
        print()
        print_header("📈 KEY LEARNING OUTCOMES")
        print("=" * 50)
        print("✅ Size Reduction: ~94% smaller images")
        print("✅ Security: Minimal attack surface")
        print("✅ Performance: Faster builds and deployments")
        print("✅ Best Practices: Multi-stage optimization")
        print("✅ Production Ready: Real-world applicable techniques")
        print()
        
        print_step("⏳ Applications will run for 10 minutes for exploration...")
        print("   • Try all three URLs to see the differences")
        print("   • Check the comparison dashboard for live metrics")
        print("   • Press Ctrl+C to stop early and keep containers running")
        time.sleep(600)

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        print("🔍 All applications are still running! Explore them:")
        print("   • Comparison Dashboard: http://localhost:8000")
        print("   • Bloated App: http://localhost:8001")
        print("   • Optimized App: http://localhost:8002")
        print()
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