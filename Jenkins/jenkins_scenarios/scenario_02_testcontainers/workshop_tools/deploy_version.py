#!/usr/bin/env python3

import subprocess
import sys
import os
import time
import shutil
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from pyfiglet import Figlet

console = Console()

# ➤ Patch PATH so docker is always found
# ------------------------------------------------------
docker_path = "/usr/local/bin"
if docker_path not in os.environ["PATH"]:
    os.environ["PATH"] += f":{docker_path}"

# ➤ Utilities
# ------------------------------------------------------

def run_cmd(command, capture_output=False, shell=True):
    """
    Run a shell command and optionally capture output.
    """
    try:
        result = subprocess.run(
            command,
            check=True,
            shell=shell,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True,
        )
        if capture_output:
            return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        console.print(f"[red]❌ Error running command:[/red] {command}")
        if e.stdout:
            console.print("[yellow]STDOUT:[/yellow]", e.stdout)
        if e.stderr:
            console.print("[yellow]STDERR:[/yellow]", e.stderr)
        sys.exit(1)

def check_docker_daemon():
    """
    Verify that Docker is running.
    """
    console.print("[cyan]🔎 Checking if Docker daemon is running...[/cyan]")
    try:
        run_cmd("docker info", capture_output=True)
        console.print("[green]✅ Docker daemon is running![/green]")
    except Exception:
        console.print("[red]❌ Docker does not seem to be running.[/red]")
        sys.exit(1)

# ➤ Deployment logic
# ------------------------------------------------------

def deploy(version):
    f = Figlet(font='slant')
    console.print(f.renderText("CI/CD Chaos Workshop"), style="bold green")
    console.print("🐍 Welcome to the CI/CD Chaos Workshop Deploy Tool 🐍\n")

    check_docker_daemon()

    console.print(f"👉 [yellow]Switching to version {version}[/yellow]\n")

    # Replace main.py
    console.print("🔄 Replacing [blue]main.py[/blue] with new version file...")
    run_cmd(f"cp app/main_v{version}.py app/main.py")

    container_name = f"chaos-app-v{version}"

    # Check for containers running on port 3000
    console.print("🔍 Checking for containers using port 3000...")
    port_in_use = run_cmd(
        "docker ps --filter 'publish=3000' --format '{{.ID}}'",
        capture_output=True
    )

    if port_in_use:
        console.print(f"⚠️ [yellow]A container is running on port 3000. Stopping and removing it...[/yellow]")
        run_cmd(f"docker stop {port_in_use}")
        run_cmd(f"docker rm {port_in_use}")

    # Remove previous container with same name
    existing = run_cmd(f"docker ps -aq -f name={container_name}", capture_output=True)
    if existing:
        console.print(f"🗑️ Removing old container named [cyan]{container_name}[/cyan]...")
        run_cmd(f"docker stop {container_name}")
        run_cmd(f"docker rm {container_name}")

    # Build image with progress spinner
    console.print("🔨 Building Docker image...")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Building Docker image...", start=False)
        progress.start_task(task)
        time.sleep(0.5)  # cosmetic delay
        run_cmd(f"docker build -t ci-cd-chaos-app:v{version} .")
        progress.update(task, description="Docker build completed!")

    # Run new container
    console.print(f"🚀 Running container [bold green]{container_name}[/bold green]...")
    run_cmd(f"docker run -d -p 3000:3000 --name {container_name} ci-cd-chaos-app:v{version}")

    # Generate Docker report
    console.print("📊 Generating Docker analysis report...")
    run_cmd(f"python3 workshop_tools/docker_analysis.py {version}")

    console.print(f"\n✅ [bold green]Deployment complete for version {version}![/bold green]")
    console.print(f"👉 View the Docker report here: [cyan]reports/version_{version}/docker_report.html[/cyan]")

# ➤ Entry point
# ------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[red]❌ Please provide a version number. Example:[/red]")
        console.print("    python deploy_version.py 2\n")
        sys.exit(1)

    version = sys.argv[1]
    deploy(version)
