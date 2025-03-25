import argparse
from flickr_api import fetch_flickr_images
from downloader import download_images
from utils import read_csv
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description="Flickr Image Downloader")
    parser.add_argument("csv_filepath",nargs="?", default="keywords.csv", type=str, help="Path to CSV file with keywords")
    parser.add_argument("age", nargs="?", default="2024-01-01", type=str, help="Oldest upload time (YYYY-MM-DD)")
    parser.add_argument("limit", type=int, nargs="?", default=10,  help="Number of images to download")
    return parser.parse_args()


def main():
    start_time = time.time()

    args = parse_arguments()
    keywords = read_csv(args.csv_filepath)

    if not keywords:
        print("No keywords found in CSV file.")
        return

    for keyword in keywords:
        print(f"Fetching images for: {keyword}")
        images = fetch_flickr_images(keyword, args.age, args.limit)
        download_images(images, keyword)

    print("Download complete. Check the 'download' folder.")

    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()
