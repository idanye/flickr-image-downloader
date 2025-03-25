import os
import json
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

DOWNLOAD_FOLDER = "download"
INDEX_FILE = os.path.join(DOWNLOAD_FOLDER, "index.json")
PROGRESS_INT = 10
MAX_THREADS = 10


def download_images(images, keyword):
    if os.path.exists(DOWNLOAD_FOLDER):
        shutil.rmtree(DOWNLOAD_FOLDER)  # Remove entire folder and its contents

    if not os.path.exists(DOWNLOAD_FOLDER):
        os.makedirs(DOWNLOAD_FOLDER)

    index_data = {"images": []}
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE, "r") as file:
            index_data = json.load(file)

    successful_downloads = 0

    def download_single_image(img, idx):
        img_url = img.get("url_s")
        if not img_url:
            return None

        img_filename = f"{keyword}_{idx}.jpg"

        img_path = os.path.join(DOWNLOAD_FOLDER, img_filename)

        max_retries = 2
        attempts = 0

        while attempts <= max_retries:
            try:
                response = requests.get(img_url, stream=True, timeout=10)
                response.raise_for_status()

                with open(img_path, "wb") as file:
                    file.write(response.content)

                print(f"Downloaded an image")

                return {"url": img_url, "keyword": keyword, "index": idx}

            except requests.exceptions.RequestException as e:
                print(f"⚠️ Attempt {attempts + 1} failed for {img_url}: {e}")
                attempts += 1

                if attempts > max_retries:
                    print(f"Failed to download {img_url}: {e}")
                    return None

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = {executor.submit(download_single_image, img, idx): idx for idx, img in enumerate(images)}

        for future in as_completed(futures):
            result = future.result()

            if result:
                index_data["images"].append(result)
                successful_downloads += 1

                # ✅ Show progress every 10 images
                if successful_downloads % 10 == 0:
                    print(f"✅ {successful_downloads} images downloaded so far...")

    with open(INDEX_FILE, "w") as file:
        json.dump(index_data, file, indent=4)

    print(f"✅ Finished downloading {successful_downloads} images for '{keyword}'")
