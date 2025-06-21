# restaurant_recommender_without_vector/scripts/recommend.py

import requests
import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from typing import List
import os

app = typer.Typer()
console = Console()

def get_recommendation(preferences: List[str]):
    """Get and display restaurant recommendation"""
    # Use localhost if running locally
    url = "http://localhost:8001/recommendations"

    try:
        # Make the API request
        response = requests.post(
            url,
            json={"preferences": preferences}
        )

        if response.status_code == 200:
            data = response.json()["formatted_response"]

            # Create a nicely formatted panel
            panel = Panel(
                Text(data, style="bright_white"),
                title="🍽️ Restaurant Recommendation",
                subtitle="based on your preferences",
                border_style="cyan",
                padding=(1, 2)
            )

            # Print the result
            console.print("\n")
            console.print(panel)
            console.print("\n")

        else:
            console.print(f"Error: {response.status_code}", style="red")

    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")

@app.command()
def search(
        preferences: List[str] = typer.Argument(
            ...,
            help="List of preferences (e.g., 'vegan' 'mexican' 'beer')"
        )
):
    """Search for restaurants based on preferences"""
    console.print(
        f"\n🔍 Searching for restaurants matching: {', '.join(preferences)}",
        style="yellow bold"
    )
    get_recommendation(preferences)

@app.command()
def interactive():
    """Interactive mode for getting recommendations"""
    console.print("\n🎉 Welcome to Restaurant Recommender!", style="bold green")

    preferences = []
    while True:
        pref = typer.prompt(
            "\nEnter a preference (or 'done' to finish)",
            default="done"
        )
        if pref.lower() == 'done':
            break
        preferences.append(pref)

    if preferences:
        console.print(
            f"\n🔍 Searching for restaurants matching: {', '.join(preferences)}",
            style="yellow bold"
        )
        get_recommendation(preferences)
    else:
        console.print("No preferences provided!", style="red")

if __name__ == "__main__":
    app()
