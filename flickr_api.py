import requests
import os
from dotenv import load_dotenv

load_dotenv()
BATCH_SIZE = 100  # Fetch in batches of 100 (Flickr's max)


def fetch_flickr_images(keyword, age, limit):
    all_images = []
    page = 1  # Start with page 1

    while len(all_images) < limit:
        params = {
            "method": "flickr.photos.search",
            "api_key": os.getenv("FLICKR_API_KEY"),
            "text": keyword,
            "format": "json",
            "nojsoncallback": 1,
            "sort": "date-posted-asc",
            "extras": "url_o,tags,title,date_upload",
            "per_page": BATCH_SIZE,
            "min_upload_date": age,
            "page": page,
        }

        try:
            response = requests.get(os.getenv("FLICKR_API_URL"), params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            photos = data.get("photos", {}).get("photo", [])

            for photo in photos:
                img_url = photo.get("url_o")
                tags = photo.get("tags", "").lower()
                title = photo.get("title", "").lower()

                # Keep only images that have a valid URL and match the keyword
                if img_url and (keyword.lower() in tags or keyword.lower() in title):
                    all_images.append(photo)

                if len(all_images) >= limit:
                    break  # Stop when we reach the limit

            if len(photos) < BATCH_SIZE:
                break  # No more pages left

            page += 1  # Fetch the next page

        except requests.exceptions.RequestException as e:
            print(f"Error fetching images for '{keyword}': {e}")
            break

    return all_images[:limit]  # Ensure exact limit

