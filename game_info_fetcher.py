import requests
import re

RAWG_ENDPOINT = "https://api.rawg.io/api/"

class GameInfoFetcher:
    """Fetches and displays details for a specified game using the RAWG API."""
    def __init__(self, api_key):
        self.api_key = api_key

    def get_game_id(self, game_name):
        """Takes hold of a specific ID for a game the user entered"""
        params = {
            "key": self.api_key,
            "search": game_name
        }
        response = requests.get(f"{RAWG_ENDPOINT}games", params=params).json()

        try:
            return response["results"][0]["id"]
        except:
            print(f"Game '{game_name}' not found.")
            return None

    def remove_html_tags(self, text):
        clean_text = re.sub(r'<.*?>', '', text)
        return clean_text

    def get_details(self, game_name):
        """Takes hold of the description of the game"""
        game_id = self.get_game_id(game_name)
        if not game_id:
            return "Unable to fetch game details."

        params = {
            "key": self.api_key,
        }
        response = requests.get(f"{RAWG_ENDPOINT}games/{game_id}", params=params).json()

        name = response.get("name", "N/A")
        description = response.get("description", "No description available")
        cleaned_description = self.remove_html_tags(description).replace("&#39;", "'")
        release_date = response.get("released", "Unknown")
        meta_score = response.get("metacritic")
        meta_score = meta_score if meta_score is not None else "No score available"
        platforms_data = response.get("platforms", [])
        platforms = [platform["platform"]["name"] for platform in platforms_data if platform.get("platform")]
        platforms_text = ", ".join(platforms) if platforms else "Not specified"
        image_url = response.get("background_image", None)

        details = (f"Game: {name}\n\nDescription: {cleaned_description}\n\nRelease Date: {release_date}\n\n"
        f"Available Platforms: {platforms_text}\n\nMetacritic Score: {meta_score}")

        return image_url, details
