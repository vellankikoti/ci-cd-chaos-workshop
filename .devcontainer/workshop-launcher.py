#!/usr/bin/env python3
"""
🚀 CI/CD Chaos Workshop Launcher for GitHub Codespaces
Automatically sets up and launches the workshop in the cloud environment
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(title):
    print(f"\n{Colors.CYAN}{'='*70}")
    print(f"🚀 {title}")
    print(f"{'='*70}{Colors.RESET}")

def print_step(step, description):
    print(f"\n{Colors.BLUE}🔧 Step {step}: {description}{Colors.RESET}")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_warning(message):
    print(f"{Colors.YELLOW}⚠️ {message}{Colors.RESET}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def run_command(cmd, description="", check=True):
    """Run a command with error handling"""
    if description:
        print(f"  {description}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=check)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, e.stdout, e.stderr

def check_environment():
    """Check if the environment is properly set up"""
    print_step(1, "Checking environment")
    
    # Check Docker
    success, _, _ = run_command("docker --version")
    if success:
        print_success("Docker is available")
    else:
        print_error("Docker is not available")
        return False
    
    # Check Kubernetes
    success, _, _ = run_command("kubectl version --client")
    if success:
        print_success("Kubernetes CLI is available")
    else:
        print_error("Kubernetes CLI is not available")
        return False
    
    # Check Python
    success, _, _ = run_command("python3 --version")
    if success:
        print_success("Python 3 is available")
    else:
        print_error("Python 3 is not available")
        return False
    
    return True

def setup_workshop():
    """Set up the workshop environment"""
    print_step(2, "Setting up workshop environment")
    
    # Change to workshop directory
    workshop_dir = Path("/workspaces/ci-cd-chaos-workshop")
    if not workshop_dir.exists():
        workshop_dir = Path.cwd()
    
    os.chdir(workshop_dir)
    
    # Set up Testcontainers
    print("  Setting up Testcontainers...")
    success, _, _ = run_command("cd testcontainers && python3 setup.py")
    if success:
        print_success("Testcontainers setup completed")
    else:
        print_warning("Testcontainers setup had issues, but continuing...")
    
    # Set up Jenkins
    print("  Setting up Jenkins...")
    success, _, _ = run_command("cd jenkins && python3 jenkins-setup.py setup")
    if success:
        print_success("Jenkins setup completed")
    else:
        print_warning("Jenkins setup had issues, but continuing...")
    
    # Set up Kubernetes
    print("  Setting up Kubernetes scenarios...")
    success, _, _ = run_command("cd kubernetes && python3 universal-setup.py")
    if success:
        print_success("Kubernetes setup completed")
    else:
        print_warning("Kubernetes setup had issues, but continuing...")
    
    return True

def show_workshop_menu():
    """Show the workshop menu"""
    print_header("🎯 CI/CD Chaos Workshop - Choose Your Adventure")
    
    print(f"{Colors.BOLD}Available Workshop Phases:{Colors.RESET}")
    print(f"  {Colors.CYAN}1. 🧪 TestContainers Chaos{Colors.RESET} - Real database testing")
    print(f"  {Colors.CYAN}2. 🐳 Docker Sabotage{Colors.RESET} - Containerization mastery")
    print(f"  {Colors.CYAN}3. 🤖 Jenkins Pipeline Showdown{Colors.RESET} - CI/CD automation")
    print(f"  {Colors.CYAN}4. ☸️ Kubernetes Warzone{Colors.RESET} - Container orchestration")
    print(f"  {Colors.CYAN}5. 🎮 Interactive Demo{Colors.RESET} - Run all scenarios")
    print(f"  {Colors.CYAN}6. 📚 Documentation{Colors.RESET} - Read the guides")
    print(f"  {Colors.CYAN}7. 🧹 Cleanup{Colors.RESET} - Reset environment")
    print(f"  {Colors.CYAN}0. 🚪 Exit{Colors.RESET}")
    
    while True:
        try:
            choice = input(f"\n{Colors.YELLOW}Enter your choice (0-7): {Colors.RESET}")
            
            if choice == "1":
                run_testcontainers_workshop()
            elif choice == "2":
                run_docker_workshop()
            elif choice == "3":
                run_jenkins_workshop()
            elif choice == "4":
                run_kubernetes_workshop()
            elif choice == "5":
                run_interactive_demo()
            elif choice == "6":
                show_documentation()
            elif choice == "7":
                cleanup_environment()
            elif choice == "0":
                print(f"\n{Colors.GREEN}Thanks for using the CI/CD Chaos Workshop!{Colors.RESET}")
                break
            else:
                print(f"{Colors.RED}Invalid choice. Please enter 0-7.{Colors.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Colors.GREEN}Goodbye!{Colors.RESET}")
            break

def run_testcontainers_workshop():
    """Run TestContainers workshop"""
    print_header("🧪 TestContainers Chaos Workshop")
    
    print("Available labs:")
    print("  1. PostgreSQL Basics")
    print("  2. Database Connections")
    print("  3. Data Management")
    print("  4. Multiple Containers")
    print("  5. Multi-Database Testing")
    print("  6. API Testing")
    print("  7. Microservices Integration")
    print("  8. Advanced Patterns")
    print("  9. Performance Testing")
    print("  10. Real-World Scenarios")
    
    choice = input("\nEnter lab number (1-10) or 'all' for all labs: ")
    
    if choice.lower() == "all":
        # Run all labs
        for i in range(1, 11):
            run_lab(f"basics/lab{i}_" if i <= 4 else f"intermediate/lab{i}_" if i <= 7 else f"advanced/lab{i}_")
    else:
        try:
            lab_num = int(choice)
            if 1 <= lab_num <= 10:
                lab_path = f"basics/lab{lab_num}_" if lab_num <= 4 else f"intermediate/lab{lab_num}_" if lab_num <= 7 else f"advanced/lab{lab_num}_"
                run_lab(lab_path)
            else:
                print(f"{Colors.RED}Invalid lab number. Please enter 1-10.{Colors.RESET}")
        except ValueError:
            print(f"{Colors.RED}Invalid input. Please enter a number or 'all'.{Colors.RESET}")

def run_lab(lab_prefix):
    """Run a specific lab"""
    print(f"\n{Colors.BLUE}Running lab: {lab_prefix}{Colors.RESET}")
    
    # Find the lab files
    testcontainers_dir = Path("testcontainers/labs")
    if not testcontainers_dir.exists():
        testcontainers_dir = Path("../testcontainers/labs")
    
    for lab_dir in ["basics", "intermediate", "advanced"]:
        lab_path = testcontainers_dir / lab_dir
        if lab_path.exists():
            for file in lab_path.glob(f"{lab_prefix}*.py"):
                print(f"  Running {file.name}...")
                success, stdout, stderr = run_command(f"cd testcontainers && python3 {file}", check=False)
                if success:
                    print_success(f"Completed {file.name}")
                else:
                    print_warning(f"Lab {file.name} had issues: {stderr}")

def run_docker_workshop():
    """Run Docker workshop"""
    print_header("🐳 Docker Sabotage Workshop")
    print("Available scenarios:")
    print("  1. Streaming Server with Docker")
    print("  2. Resilience Engineering")
    print("  3. Networking Chaos")
    print("  4. Multi-stage Builds")
    print("  5. Security Scanning")
    
    print(f"\n{Colors.YELLOW}Navigate to Docker scenarios directory and follow the guides:{Colors.RESET}")
    print("  cd docker/docker-scenarios")
    print("  ls -la  # See available scenarios")

def run_jenkins_workshop():
    """Run Jenkins workshop"""
    print_header("🤖 Jenkins Pipeline Showdown")
    
    # Check if Jenkins is running
    success, _, _ = run_command("docker ps --filter name=jenkins-workshop")
    if success:
        print_success("Jenkins is running!")
        print(f"\n{Colors.GREEN}Jenkins URL: http://localhost:8080{Colors.RESET}")
        print(f"{Colors.GREEN}Username: admin{Colors.RESET}")
        print(f"{Colors.GREEN}Password: admin{Colors.RESET}")
        
        # Try to open Jenkins in browser
        try:
            webbrowser.open("http://localhost:8080")
        except:
            print(f"{Colors.YELLOW}Please open http://localhost:8080 in your browser{Colors.RESET}")
    else:
        print_warning("Jenkins is not running. Starting it...")
        success, _, _ = run_command("cd jenkins && python3 jenkins-setup.py setup")
        if success:
            print_success("Jenkins started successfully!")
        else:
            print_error("Failed to start Jenkins")

def run_kubernetes_workshop():
    """Run Kubernetes workshop"""
    print_header("☸️ Kubernetes Warzone")
    
    # Check if any Kubernetes cluster is available
    success, _, _ = run_command("kubectl get nodes")
    if success:
        print_success("Kubernetes cluster is accessible!")
        
        # Check if it's Kind cluster specifically
        kind_success, _, _ = run_command("kind get clusters")
        if kind_success:
            print_success("Kind cluster is running!")
        else:
            print_info("Using default Kubernetes cluster (Kind not available)")
        
        print(f"\n{Colors.GREEN}Available scenarios:{Colors.RESET}")
        print("  1. Python App Deployment")
        print("  2. Secret Automation")
        print("  3. Blue-Green Deployments")
        print("  4. Auto-scaling")
        print("  5. GitOps")
        
        print(f"\n{Colors.YELLOW}Navigate to Kubernetes scenarios:{Colors.RESET}")
        print("  cd kubernetes/kubernetes-scenarios")
        print("  ls -la  # See available scenarios")
        
        print(f"\n{Colors.CYAN}Quick start:{Colors.RESET}")
        print("  kubectl get nodes  # Check cluster status")
        print("  kubectl get pods --all-namespaces  # See all pods")
    else:
        print_warning("Kubernetes cluster is not accessible.")
        print(f"\n{Colors.YELLOW}This might be due to Docker-in-Docker limitations in Codespaces.{Colors.RESET}")
        print(f"\n{Colors.CYAN}Alternative options:{Colors.RESET}")
        print("  1. Use a cloud Kubernetes cluster (GKE, EKS, AKS)")
        print("  2. Use local installation with Docker Desktop")
        print("  3. Try running: kubectl config get-contexts")

def run_interactive_demo():
    """Run interactive demo"""
    print_header("🎮 Interactive Demo")
    print("This will run a comprehensive demo of all workshop components...")
    
    # Run a sample from each phase
    print("\n🧪 TestContainers Demo...")
    run_command("cd testcontainers && python3 labs/basics/lab1_postgresql_basics.py")
    
    print("\n🐳 Docker Demo...")
    run_command("cd docker && ls -la docker-scenarios/")
    
    print("\n🤖 Jenkins Demo...")
    run_command("cd jenkins && python3 jenkins-setup.py status")
    
    print("\n☸️ Kubernetes Demo...")
    run_command("kubectl get nodes")

def show_documentation():
    """Show documentation"""
    print_header("📚 Workshop Documentation")
    
    docs = [
        ("README.md", "Main workshop guide"),
        ("testcontainers/README.md", "TestContainers guide"),
        ("jenkins/README.md", "Jenkins guide"),
        ("kubernetes/README.md", "Kubernetes guide"),
        ("docker/README.md", "Docker guide")
    ]
    
    for doc, description in docs:
        if Path(doc).exists():
            print(f"  📖 {doc} - {description}")
        else:
            print(f"  ❌ {doc} - {description} (not found)")
    
    print(f"\n{Colors.YELLOW}To read a specific guide:{Colors.RESET}")
    print("  cat README.md")
    print("  cat testcontainers/README.md")

def cleanup_environment():
    """Clean up the environment"""
    print_header("🧹 Cleaning Up Environment")
    
    print("This will clean up all workshop resources...")
    confirm = input("Are you sure? (y/N): ")
    
    if confirm.lower() == 'y':
        print("Cleaning up Jenkins...")
        run_command("cd jenkins && python3 jenkins-setup.py cleanup", check=False)
        
        print("Cleaning up Kubernetes...")
        run_command("kind delete cluster --name chaos-workshop", check=False)
        
        print("Cleaning up Docker...")
        run_command("docker system prune -f", check=False)
        
        print_success("Cleanup completed!")
    else:
        print("Cleanup cancelled.")

def main():
    """Main function"""
    print_header("Welcome to CI/CD Chaos Workshop!")
    print("This workshop runs entirely in GitHub Codespaces - no local setup required!")
    
    if not check_environment():
        print_error("Environment check failed. Please check the setup.")
        return
    
    if not setup_workshop():
        print_error("Workshop setup failed. Please check the logs.")
        return
    
    show_workshop_menu()

if __name__ == "__main__":
    main()
