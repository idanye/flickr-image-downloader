import requests
import os
from dotenv import load_dotenv

load_dotenv()


def fetch_flickr_images(keyword, age, limit):
    params = {
        "method": "flickr.photos.search",
        "api_key": os.getenv("FLICKR_API_KEY"),
        "text": keyword,
        "format": "json",
        "nojsoncallback": 1,
        "sort": "date-posted-asc",
        "extras": "url_o,date_upload",
        "per_page": limit,
        "min_upload_date": age,
    }

    try:
        response = requests.get(os.getenv("FLICKR_API_URL"), params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        return data.get("photos", {}).get("photo", [])

    except requests.exceptions.RequestException as e:
        print(f"Error fetching images for '{keyword}': {e}")
        return []
