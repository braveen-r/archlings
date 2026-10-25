import typer
import yaml
import os
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from archlings.runner.docker import start_scenario
from archlings.progress import db

app = typer.Typer(help="Archlings: The Arch Linux Troubleshooting Trainer")
console = Console()

@app.command()
def start(scenario_id: str):
    """Start a specific troubleshooting scenario."""
    scenario_dir = f"scenarios/{scenario_id}"
    
    if not os.path.exists(scenario_dir):
        console.print(f"[bold red]❌ Scenario '{scenario_id}' not found.[/]")
        raise typer.Exit(1)
        
    with open(os.path.join(scenario_dir, "scenario.yml"), "r") as f:
        config = yaml.safe_load(f)
        
    console.print(Panel.fit(
        f"[bold yellow]Scenario:[/] {config['title']}\n"
        f"[bold yellow]Difficulty:[/] {config['difficulty']}\n\n"
        f"{config['description']}",
        title=f"🐧 Archlings: {scenario_id}",
        border_style="cyan"
    ))
    
    db.mark_started(scenario_id)
    start_scenario(scenario_id, scenario_dir)

@app.command()
def verify(scenario_id: str):
    """Verify if the running scenario is fixed."""
    container_name = f"archlings-{scenario_id}"
    
    result = subprocess.run(["docker", "ps", "-q", "-f", f"name={container_name}"], capture_output=True, text=True)
    if not result.stdout.strip():
        console.print(f"[bold red]❌ Container '{container_name}' is not running.[/]")
        raise typer.Exit(1)
        
    console.print(f"[bold cyan]🔍 Verifying fix inside the container...[/]")
    exec_result = subprocess.run(["docker", "exec", container_name, "/bin/bash", "/lab/verify.sh"])
    
    if exec_result.returncode == 0:
        stats = db.mark_completed(scenario_id)
        duration_sec = stats[0]
        mins, secs = divmod(duration_sec, 60)
        console.print(f"\n[bold green]🎉 Great job! You repaired the system in {mins}m {secs}s![/]")
    else:
        console.print("\n[bold red]❌ The system is still broken. Keep trying![/]")

@app.command()
def progress():
    """View your training progress."""
    records = db.get_all_progress()
    table = Table(title="Archlings Training Progress")
    table.add_column("Scenario ID", style="cyan")
    table.add_column("Status", style="magenta")
    table.add_column("Hints Used", justify="right")
    
    for row in records:
        status_emoji = "✅ Completed" if row[1] == 'completed' else "⏳ In Progress"
        table.add_row(row[0], status_emoji, str(row[2]))
        
    console.print(table)

if __name__ == "__main__":
    app()
