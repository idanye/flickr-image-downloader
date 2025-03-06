import os
import json
import requests

DOWNLOAD_FOLDER = "download"
INDEX_FILE = os.path.join(DOWNLOAD_FOLDER, "index.json")


def download_images(images, keyword):
    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    index_data = {"images": []}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as file:
            index_data = json.load(file)

    for idx, img in enumerate(images):
        img_url = img.get("url_o")
        if not img_url:
            continue

        img_filename = f"{keyword}_{idx}.jpg"
        img_path = os.path.join(DOWNLOAD_FOLDER, img_filename)

        try:
            response = requests.get(img_url, stream=True, timeout=10)
            response.raise_for_status()

            with open(img_path, "wb") as file:
                file.write(response.content)

            index_data["images"].append({
                "url": img_url,
                "keyword": keyword,
                "index": len(index_data["images"])
            })

        except requests.exceptions.RequestException as e:
            print(f"Failed to download {img_url}: {e}")

    with open(INDEX_FILE, "w") as file:
        json.dump(index_data, file, indent=4)
