"""
Governance Scanner CLI

Command-line tool for scanning and validating governance policies.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="tork",
    help="Tork Governance CLI - Universal governance tools for AI agents",
)
console = Console()


@app.command()
def scan(
    policy: Path = typer.Option(
        ...,
        "--policy",
        "-p",
        help="Path to policy file or directory",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output",
    ),
) -> None:
    """Scan and validate governance policies."""
    console.print(f"[bold blue]Tork Governance Scanner[/bold blue]")
    console.print(f"Scanning policies at: {policy}")
    
    if not policy.exists():
        console.print(f"[red]Error: Path does not exist: {policy}[/red]")
        raise typer.Exit(1)
    
    from tork.compliance import PolicyValidator
    
    validator = PolicyValidator()
    count = validator.load_policies(policy)
    
    console.print(f"[green]Loaded {count} policies[/green]")
    
    if verbose:
        table = Table(title="Policy Summary")
        table.add_column("Policy", style="cyan")
        table.add_column("Status", style="green")
        table.add_row("Governance policies", f"{count} loaded")
        console.print(table)


@app.command()
def version() -> None:
    """Display version information."""
    from tork import __version__
    console.print(f"Tork Governance SDK v{__version__}")


@app.command()
def init(
    output: Path = typer.Option(
        Path("./policies"),
        "--output",
        "-o",
        help="Output directory for policy templates",
    ),
) -> None:
    """Initialize a new policy directory with templates."""
    output.mkdir(parents=True, exist_ok=True)
    console.print(f"[green]Created policy directory: {output}[/green]")
    console.print("Add your YAML policy files to this directory.")


if __name__ == "__main__":
    app()
