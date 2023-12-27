from rich.console import Console

console = Console()


def success(message):
    console.print(f"SUCCESS: {message}", style="bold green")

def info(message):
    console.print(f"INFO: {message}")

def warn(message):
    console.print(f"WARN: {message}", style="bold yellow")

def error(message):
    console.print(f"ERROR: {message}", style="bold red")
