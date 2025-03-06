# Flickr Image Downloader

## Overview
This is a **command-line tool** that downloads images from Flickr based on keywords provided in a CSV file. The tool saves images in a `download/` folder and generates an `index.json` file containing metadata about the downloaded images.

## Features
✅ Fetches images from **Flickr API** using given keywords.  
✅ Filters images to ensure **relevance to the keyword**.  
✅ Ensures **the exact number of images** is downloaded (even if pagination is required).  
✅ Saves metadata in `index.json`.  
✅ Uses a `.env` file to store the API key securely.

## Installation
1. **Clone the repository**
   ```sh
   git clone https://github.com/your-repo/flickr-downloader.git
   cd flickr-downloader
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up API key**
   - Create a `.env` file in the root directory:
     ```sh
     touch .env
     ```
   - Add your Flickr API key inside `.env`:
     ```sh
     FLICKR_API_KEY=your_api_key_here
     ```

## Usage
Run the script using:
```sh
python main.py <csv_file> <age> <limit>
```
### Example
```sh
python main.py keywords.csv 2024-01-01 10
```
- **`keywords.csv`** → CSV file with keywords (one per line, e.g., cat, dog, car).  
- **`2024-01-01`** → Oldest upload date for images.  
- **`10`** → Number of images per keyword.

## Output
- Images are saved inside the `download/` folder.
- An `index.json` file is generated with metadata:
  ```json
  {
    "images": [
      {
        "url": "https://flickr.com/sample.jpg",
        "keyword": "cat",
        "index": 0
      }
    ]
  }
  ```

## File Structure
```
📂 flickr_downloader/
│── main.py         # Entry point
│── flickr_api.py   # Handles API requests
│── downloader.py   # Downloads images & updates index.json
│── utils.py        # Reads CSV file
│── .env            # Stores API key (not committed)
│── requirements.txt # Dependencies
│── README.md       # Documentation
│── download/       # Stores images & index.json
```

## Dependencies
- Python 3.8+
- `requests`
- `python-dotenv`

## Notes
- Ensure your **Flickr API key** has access to the required endpoints.
- If an image **does not have a valid URL**, it will be skipped.
- **Flickr search is not perfect**, but the script improves accuracy by filtering images based on **title and tags**.

## License
MIT License
