import json
import shutil
import time
import typer
import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.align import Align

from ricevault.utils import ensure_vault, VAULT_DIR, take_screenshot
from ricevault.backup import create_backup
from ricevault.restore import restore_rice, validate_rice

app = typer.Typer(help="RiceVault - Git for KDE Plasma Rices")
console = Console()

@app.command()
def info():
    """Display developer and project information."""
    from rich.console import Console
    from rich.panel import Panel
    from rich.align import Align

    console = Console()

    content = """
[bold cyan]🍚 RiceVault v1.0[/bold cyan]
The Ultimate KDE Plasma Profile Manager

[bold]👤 Created by:[/bold] Tacenta
[bold]📧 Contact:[/bold] aswingopakumarx@gmail.com

[bold pink]💖 Support the Project & Buy me a Coffee:[/bold pink]
[bold green]☕ Ko-fi:[/bold green]  https://ko-fi.com/tacenta
[bold green]💸 UPI:[/bold green]    aswingk@ptyes
[bold green]⭐ GitHub:[/bold green] github.com/TacentaXT
    """

    panel = Panel(
        Align.center(content),
        border_style="cyan",
        title="Welcome to RiceVault",
        subtitle="Open Source"
    )

    console.print("\n")
    console.print(panel)
    console.print("\n")

@app.command(name="list")
def list_rices():
    """List all saved KDE Plasma rices."""
    ensure_vault()

    rices = [d for d in VAULT_DIR.iterdir() if d.is_dir()]

    if not rices:
        console.print("[yellow]Your vault is empty! Run `rice backup` to save your first setup.[/yellow]")
        return

    table = Table(title="🍚 Saved Rices in Vault", border_style="cyan", title_justify="left")
    table.add_column("Name", style="bold green")
    table.add_column("Created", style="cyan")
    table.add_column("Type", style="magenta")
    table.add_column("Plasma", style="dim")

    for rice_dir in sorted(rices):
        meta_path = rice_dir / "metadata.json"
        if meta_path.exists():
            try:
                with open(meta_path, "r") as f:
                    meta = json.load(f)

                name = meta.get("name", rice_dir.name)
                created = meta.get("created", "Unknown").replace("T", " ")
                b_type = meta.get("backup_type", "Unknown")
                plasma = meta.get("plasma_version", "Unknown")

                table.add_row(name, created, b_type, plasma)
            except json.JSONDecodeError:
                table.add_row(rice_dir.name, "[red]Corrupted metadata[/red]", "-", "-")
        else:
            table.add_row(rice_dir.name, "Legacy/Unknown", "-", "-")

    console.print(table)

@app.command()
def delete(name: str = typer.Argument(None, help="Name of the rice to delete (optional)")):
    """Delete a saved rice safely."""
    ensure_vault()

    rices = [d.name for d in VAULT_DIR.iterdir() if d.is_dir()]

    if not rices:
        console.print("[yellow]Your vault is empty! Nothing to delete.[/yellow]")
        return

    if not name:
        name = questionary.select(
            "Select a rice to delete:",
            choices=rices
        ).ask()

        if not name:
            console.print("[dim]Deletion cancelled.[/dim]")
            raise typer.Exit()

    rice_dir = VAULT_DIR / name

    if not rice_dir.exists() or not rice_dir.is_dir():
        console.print(f"[bold red]Error:[/bold red] Rice '{name}' not found in the vault.")
        raise typer.Exit(1)

    confirm = questionary.confirm(
        f"Are you absolutely sure you want to delete '{name}'? This cannot be undone.",
        default=False
    ).ask()

    if confirm:
        try:
            shutil.rmtree(rice_dir)
            console.print(f"[bold green]✓ Successfully deleted '{name}'[/bold green]")
        except Exception as e:
            console.print(f"[bold red]Error deleting '{name}':[/bold red] {e}")
    else:
        console.print("[dim]Deletion cancelled.[/dim]")

@app.command()
def backup():
    """Launch the interactive Backup Wizard."""
    ensure_vault()

    console.print(Panel("[bold green]🍚 RiceVault Backup Wizard[/bold green]", expand=False))

    console.print("\n[bold cyan]Step 1/6[/bold cyan]")
    rice_name = questionary.text("Name of this rice:").ask()
    if not rice_name:
        raise typer.Exit()

    console.print("\n[bold cyan]Step 2/6[/bold cyan]")
    preview_choice = questionary.select(
        "Preview Image:",
        choices=["Skip", "Existing image", "Screenshot"]
    ).ask()

    preview_path = None
    if preview_choice == "Existing image":
        preview_path = questionary.path("Path to image:").ask()
    elif preview_choice == "Screenshot":
        timer_input = questionary.text(
            "Delay in seconds before screenshot:",
            default="3",
            validate=lambda text: text.isdigit() and int(text) >= 0 or "Please enter a valid number of seconds."
        ).ask()

        if timer_input is None:
            raise typer.Exit()

        timer = int(timer_input)

        if timer > 0:
            console.print(f"[dim]Prepare your desktop... taking screenshot in {timer} seconds.[/dim]")
            for i in range(timer, 0, -1):
                with console.status(f"[bold yellow]{i}..."):
                    time.sleep(1)
        else:
            console.print("[dim]Taking screenshot immediately...[/dim]")

        preview_path = take_screenshot()
        if preview_path:
            console.print("[bold green]✓ Screenshot captured![/bold green]")
        else:
            console.print("[bold red]✗ Failed to take screenshot. (Is spectacle installed?)[/bold red]")

    console.print("\n[bold cyan]Step 3/6[/bold cyan]")
    backup_type = questionary.select(
        "Backup type:",
        choices=["Full", "Theme only", "Custom"]
    ).ask()

    custom_components = []
    if backup_type == "Custom":
        custom_components = questionary.checkbox(
            "Select components to backup:",
            choices=["Wallpaper", "KWin Rules", "Panels", "Widgets", "Shortcuts"]
        ).ask()

    console.print("\n[bold cyan]Step 4/6[/bold cyan]")
    apps = questionary.checkbox(
        "Include application configs:",
        choices=["Konsole", "Dolphin", "Kate"]
    ).ask()

    console.print("\n[bold cyan]Step 5/6[/bold cyan]")
    include_packages = questionary.confirm(
        "Detect and include package list (Arch/AUR)?",
        default=True
    ).ask()

    console.print("\n[bold cyan]Step 6/6: Summary[/bold cyan]")
    summary_text = (
        f"[bold]Name:[/bold] {rice_name}\n"
        f"[bold]Type:[/bold] {backup_type}\n"
        f"[bold]Apps:[/bold] {', '.join(apps) if apps else 'None'}"
    )
    console.print(Panel(summary_text, title="Confirm Backup", border_style="green", expand=False))

    confirm = questionary.confirm("Create this backup now?", default=True).ask()

    if confirm:
        with console.status(f"[bold green]Creating '{rice_name}' backup..."):
            try:
                result = create_backup(
                    name=rice_name, backup_type=backup_type, custom_components=custom_components,
                    apps=apps, include_packages=include_packages, preview_path=preview_path
                )

                # --- NEW SUCCESS SCREEN ---
                backup_path = str(VAULT_DIR / rice_name)

                success_content = f"""
[bold green]✔ Success! Your desktop configuration has been secured.[/bold green]

[bold]📁 Saved Location:[/bold]
[cyan]{backup_path}[/cyan]

[bold]📦 Captured Elements:[/bold]
• KDE Panel & Layouts (`plasmashellrc`)
• Color Schemes & Accents (`kdeglobals`)
• Window Rules & Borders (`kwinrc`)
"""
                console.print("\n")
                console.print(
                    Panel(
                        Align.left(success_content),
                        title="[bold green]Backup Complete[/bold green]",
                        border_style="green",
                        expand=False
                    )
                )
                console.print(
                    "[dim]💡 Tip: Run [bold cyan]rice list[/bold cyan] to see all your secured profiles.[/dim]\n"
                )

            except Exception as e:
                console.print(f"\n[bold red]Error:[/bold red] {e}")
    else:
        console.print("\n[red]Backup cancelled.[/red]")

@app.command()
def restore():
    """Launch the interactive Restore Wizard."""
    ensure_vault()

    console.print(Panel("[bold blue]🍚 RiceVault Restore Wizard[/bold blue]", expand=False))

    rices = [d.name for d in VAULT_DIR.iterdir() if d.is_dir() and validate_rice(d.name)]

    if not rices:
        console.print("[yellow]No valid backups found in the vault.[/yellow]")
        raise typer.Exit()

    # Step 1: Select Rice
    console.print("\n[bold cyan]Step 1/6[/bold cyan]")
    rice_name = questionary.select(
        "Select a rice to restore:",
        choices=rices
    ).ask()

    if not rice_name:
        raise typer.Exit()

    # Step 2: Profile Info
    console.print("\n[bold cyan]Step 2/6[/bold cyan]")
    meta_path = VAULT_DIR / rice_name / "metadata.json"
    with open(meta_path, "r") as f:
        meta = json.load(f)

    info_text = (
        f"[bold]Name:[/bold] {meta.get('name', rice_name)}\n"
        f"[bold]Type:[/bold] {meta.get('backup_type', 'Unknown')}\n"
        f"[bold]Plasma Version:[/bold] {meta.get('plasma_version', 'Unknown')}\n"
        f"[bold]Apps Included:[/bold] {', '.join(meta.get('apps_included', [])) or 'None'}"
    )
    console.print(Panel(info_text, title="Profile Info", border_style="blue", expand=False))
    questionary.confirm("Continue with this profile?", default=True).ask()

    # Step 3 & 4: Scope and Dependencies
    console.print("\n[bold cyan]Step 3/6 & Step 4/6[/bold cyan]")
    console.print("[dim]Partial restores and package detection will be enabled in Phase 3. Defaulting to Full Restore.[/dim]")

    # Step 5: Failsafe
    console.print("\n[bold cyan]Step 5/6: Failsafe[/bold cyan]")
    console.print("[yellow]☑ A mandatory Emergency Backup will be created before any files are modified.[/yellow]")

    # Step 6: Summary & Execution
    console.print("\n[bold cyan]Step 6/6: Confirm[/bold cyan]")
    confirm = questionary.confirm(f"Are you sure you want to apply '{rice_name}'?", default=False).ask()

    if confirm:
        with console.status(f"[bold blue]Restoring '{rice_name}' (this might take a moment)..."):
            try:
                result = restore_rice(rice_name)
                console.print(f"\n[bold green]✓ Successfully restored '{rice_name}'![/bold green]")
                console.print(f"[dim]Emergency Backup created: {result['emergency_backup']}[/dim]")
                console.print(f"[dim]Restored {result['restored_items']} components.[/dim]")
                console.print("\n[bold yellow]Note:[/bold yellow] Please log out and log back in for changes to take full effect.")
            except Exception as e:
                console.print(f"\n[bold red]Error restoring rice:[/bold red] {e}")
    else:
        console.print("\n[dim]Restore cancelled. Your system was not modified.[/dim]")

@app.command()
def help():
    """Display the RiceVault help menu and available commands."""
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.align import Align

    console = Console()

    # Create a beautiful table
    table = Table(show_header=True, header_style="bold cyan", border_style="cyan", expand=False)
    table.add_column("Command", style="bold green", width=15)
    table.add_column("Description", style="white")

    # Add the commands
    table.add_row("rice backup", "Save your current KDE Plasma configuration and themes.")
    table.add_row("rice restore", "Load and apply a previously saved KDE Plasma configuration.")
    table.add_row("rice info", "Display developer, project, and contact information.")

    # Wrap it in a sleek panel
    panel = Panel(
        Align.center(table),
        title="[bold cyan]RiceVault Commands[/bold cyan]",
        border_style="cyan",
        expand=False
    )

    console.print("\n")
    console.print(Align.center(panel))
    console.print("\n")

if __name__ == "__main__":
    app()
