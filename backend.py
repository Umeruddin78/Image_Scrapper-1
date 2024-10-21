import requests
import json


api_key = "1b22ad0fd3485ffa1027b3881634b409372ffa47661f0f5f31d60f098e8c809b"   #Umeruddin

def scrape_google_images(query, num_images=50):

    search_url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "tbm": "isch",
        "ijn": 0,
        "api_key": api_key
    }

    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        search_results = response.json()

        # Extract the image URLs from the search results
        image_urls = [result["original"] for result in search_results["images_results"][:num_images]]
        return image_urls

    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        print(f"No or bad internet connection")
        return None
