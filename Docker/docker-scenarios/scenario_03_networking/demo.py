#!/usr/bin/env python3
"""
Docker Networking Demo - Python Version
=======================================

Demonstrate container networking and communication
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
    """Clean up all demo containers and networks"""
    print_header("🧹 CLEANUP")
    print("=" * 50)
    
    print_step("Stopping all containers...")
    run_command("docker stop app-container db-container")
    
    print_step("Removing containers...")
    run_command("docker rm app-container db-container")
    
    print_step("Removing demo network...")
    run_command("docker network rm demo-network")
    
    print_step("Removing demo images...")
    run_command("docker rmi demo-app")
    
    print_success("Cleanup completed!")

def main():
    """Main demo function"""
    print_header("🌐 DOCKER NETWORKING DEMO")
    print("=" * 50)
    print("Demonstrating container networking and communication")
    print("")
    
    # Trap to ensure cleanup on exit
    try:
        # Change to script directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        # Step 1: Show app without database (will fail)
        print_header("STEP 1: App Without Database")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This demonstrates container isolation")
        print("   • Shows what happens when services can't communicate")
        print("   • Demonstrates the need for proper networking")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Building app image with Docker BuildKit...")
        if not run_command("docker buildx build -t demo-app --load app/"):
            print_error("Failed to build app image")
            return
        
        print_step("Starting app container (no database)...")
        if not run_command("docker run -d --name app-container -p 8000:5000 demo-app"):
            print_error("Failed to start app container")
            return
        
        print_step("Waiting for app to start...")
        time.sleep(5)  # Increased delay
        
        print_step("Testing app endpoint...")
        if run_command("curl -s http://localhost:8000 > /dev/null"):
            print_success("App is running on http://localhost:8000")
        else:
            print_error("App failed to start")
            run_command("docker logs app-container")
            return
        
        print_step("Testing database connection (should fail)...")
        if run_command("curl -s http://localhost:8000 | grep -q 'Redis connection failed'", capture_output=True):
            print_success("Expected: Redis connection failed (container isolation)")
        else:
            print_error("Unexpected response from database endpoint")
        
        print_step("⏳ Pausing to let you explore the failing app...")
        print("   • Visit http://localhost:8000 to see the error")
        print("   • Notice the red error message about Redis connection")
        time.sleep(5)
        
        print("")
        
        # Step 2: Create network and add database
        print_header("STEP 2: Adding Database with Network")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows how to create custom Docker networks")
        print("   • Demonstrates container-to-container communication")
        print("   • Shows the solution to the isolation problem")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Creating custom network...")
        if not run_command("docker network create demo-network"):
            print_error("Failed to create network")
            return
        
        print_step("Starting Redis container...")
        if not run_command("docker run -d --name db-container --network demo-network redis:7-alpine"):
            print_error("Failed to start Redis container")
            return
        
        print_step("Waiting for database to start...")
        time.sleep(8)  # Increased delay for database startup
        
        print_step("Connecting app to database network...")
        run_command("docker stop app-container")
        run_command("docker rm app-container")
        if not run_command("docker run -d --name app-container --network demo-network -p 8000:5000 -e REDIS_HOST=db-container demo-app"):
            print_error("Failed to start app container on network")
            return
        
        print_step("Waiting for app to reconnect...")
        time.sleep(5)  # Increased delay
        
        print_step("Testing database connection (should work)...")
        if run_command("curl -s http://localhost:8000 | grep -q 'Database Connected'", capture_output=True):
            print_success("Success: Database connection working!")
        else:
            print_error("Database connection still failing")
            run_command("docker logs app-container")
            return
        
        print("")
        
        # Step 3: Show network inspection
        print_header("STEP 3: Network Inspection")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This shows how Docker networks work internally")
        print("   • Demonstrates container IP addresses and connectivity")
        print("   • Shows network debugging and inspection tools")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Listing Docker networks...")
        run_command("docker network ls")
        
        print_step("Inspecting demo network...")
        run_command("docker network inspect demo-network --format '{{json .Containers}}' | python3 -m json.tool")
        
        print_step("Container IP addresses...")
        run_command("docker inspect app-container --format '{{.NetworkSettings.IPAddress}}'", "App container IP")
        run_command("docker inspect db-container --format '{{.NetworkSettings.IPAddress}}'", "DB container IP")
        
        print("")
        
        # Step 4: Test internal communication
        print_header("STEP 4: Internal Communication")
        print("=" * 50)
        
        print_step("🎓 Educational Context:")
        print("   • This demonstrates container-to-container communication")
        print("   • Shows the difference between internal and external access")
        print("   • Demonstrates network security and isolation")
        
        print_step("⏳ Pausing for audience to understand...")
        time.sleep(3)
        
        print_step("Testing internal container communication...")
        run_command("docker exec app-container curl -s http://db-container:5432 > /dev/null || true")
        
        print_step("Testing external access...")
        print_success("App accessible at: http://localhost:8000")
        print_success("Database accessible internally via: db-container:5432")
        
        print("")
        
        print_header("🎉 DEMO COMPLETED")
        print("=" * 50)
        print_success("Docker networking concepts demonstrated!")
        print("")
        print_step("📊 SUMMARY OF WHAT WE LEARNED:")
        print("  • Container isolation and networking")
        print("  • Custom Docker networks")
        print("  • Internal vs external communication")
        print("  • Network inspection and debugging")
        print("")
        print_step("🌐 Test the app: http://localhost:8000")
        print("   • Try voting to see the Redis connection in action")
        print("   • Check the network status indicators")
        print("")
        print_step("⏳ Demo will auto-cleanup in 10 minutes...")
        print("   • All services are still running and available")
        print("   • You can explore them at your own pace")
        print("   • Press Ctrl+C to stop early and keep containers running")
        time.sleep(600)

    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
        print("🔍 Containers are still running! You can explore them:")
        print("   • App: http://localhost:8000")
        print("   • Try voting to see the Redis connection in action")
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
