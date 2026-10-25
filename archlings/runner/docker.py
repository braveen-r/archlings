import subprocess
import os
from rich.console import Console

console = Console()

def build_base_image_if_missing():
    result = subprocess.run(["docker", "images", "-q", "archlings-base"], capture_output=True, text=True)
    if not result.stdout.strip():
        console.print("[bold cyan]🔨 Building base Arch Linux lab image (this takes ~1 min the first time)...[/]")
        subprocess.run(
            ["docker", "build", "-t", "archlings-base", "-f", "docker/Dockerfile.arch-lab", "."],
            check=True
        )

def start_scenario(scenario_id: str, scenario_dir: str):
    build_base_image_if_missing()
    
    console.print(f"[bold green]🚀 Dropping you into the broken lab environment...[/]")
    console.print("[dim]Type 'exit' when you are done practicing.[/dim]\n")
    
    abs_scenario_dir = os.path.abspath(scenario_dir)
    container_name = f"archlings-{scenario_id}"
    
    # Clean up any leftover container from previous runs
    subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
    
    # Mount the scenario folder so the container can access setup.sh and verify.sh
    cmd = [
        "docker", "run", "-it", "--rm",
        "--name", container_name,
        "-v", f"{abs_scenario_dir}:/lab",
        "-w", "/root",
        "archlings-base",
        "/bin/bash", "-c", "/lab/setup.sh && exec /bin/bash"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        pass
