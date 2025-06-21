# test_recommend.py
import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

app = typer.Typer()
console = Console()

def get_recommendation(preferences: list):
    url = "http://localhost:8001/recommendations"
    response = requests.post(
        url,
        json={"preferences": preferences}
    )

    if response.status_code == 200:
        formatted_response = response.json()["formatted_response"]

        # Create styled panel
        panel = Panel(
            Text(formatted_response, style="bright_white"),
            title="🎯 Restaurant Recommendation",
            subtitle="powered by AI",
            border_style="cyan"
        )

        console.print(panel)
    else:
        console.print(f"Error: {response.status_code}", style="red")

@app.command()
def recommend(preferences: list[str]):
    """Get restaurant recommendations based on your preferences"""
    console.print(f"\n🔍 Searching for restaurants matching: {', '.join(preferences)}\n", style="yellow")
    get_recommendation(preferences)

if __name__ == "__main__":
    app()
