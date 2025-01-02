# Instagram Video Downloader and Uploader Bot

## Project Overview

This project is a Python-based bot that downloads Instagram videos from provided URLs, uploads them to an API, and posts them on a social media platform. It also includes monitoring functionality for automatically processing newly added `.mp4` files in a specific directory.

### Features
- Downloads Instagram videos from provided post URLs.
- Uploads downloaded videos to a remote API.
- Creates posts with the uploaded videos.
- Automatically processes newly added `.mp4` files in a specified directory.
- Deletes local video files after upload to conserve space.

---

## Table of Contents

1. [Setup Instructions](#setup-instructions)
2. [Usage Guidelines](#usage-guidelines)
3. [Code Comments](#code-comments)
4. [README Quality](#readme-quality)
5. [License](#license)

---

## Setup Instructions

### Prerequisites

Ensure the following are installed:

- Python 3.6 or higher
- `pip` (Python package manager)

### Step 1: Install Dependencies

Clone the repository to your local machine (or download the code files).

```bash
git clone https://github.com/yourusername/instagram-video-bot.git
cd instagram-video-bot
Install the required Python packages using pip.

bash
Copy code
pip install -r requirements.txt
This will install the necessary libraries:

aiohttp: For asynchronous HTTP requests.
instaloader: For downloading Instagram content.
watchdog: To monitor the directory for new .mp4 files.

Step 2: Configure API Token
You will need to obtain an API token from the target social media API and update it in the script.

In the file main.py, replace the placeholder token with your own:

python
Copy code
FLIC_TOKEN = "your_actual_flic_token_here"
Ensure that your API URL and other configurations match your requirements.

Step 3: Set Directory Path
In the script, set the directory path where videos will be downloaded and monitored:

python
Copy code
download_path = r"C:\Users\YourUsername\video-bot\videos"
This should be an existing directory on your system. Make sure that this directory is writable.

Usage Guidelines
Step 1: Running the Script
To begin processing videos, simply run the script:

bash
Copy code
python main.py
This will start the process of downloading videos from Instagram URLs, uploading them to the API, creating posts, and monitoring the video folder for new .mp4 files.

Step 2: Handling New Videos
When new .mp4 files are added to the directory specified in download_path, the bot will automatically detect and process them.

Video Downloading: The bot downloads the video from the provided Instagram post URL and saves it to the specified folder.
Video Uploading: The bot uploads the video to the remote API using the provided upload_url.
Creating Posts: After uploading, the bot creates a new post with the uploaded video on the platform.
Deleting Local Files: Once the post is successfully created, the bot deletes the local video file to avoid clutter.
Step 3: Monitoring for New Files
The bot will continue to run and monitor the folder for new .mp4 files. If a new file is detected, it will trigger the process to download and upload it automatically.

Example Usage:
Add Instagram video URLs to the instagram_video_urls list in the script:
python
Copy code
instagram_video_urls = [
    "https://www.instagram.com/p/B-65ymYAUoo/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
    "https://www.instagram.com/p/B9gxxoDAXw9/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
]
Code Comments
Below is a description of key functions and their role within the bot:

download_instagram_content(url, download_path)
Purpose: Downloads an Instagram video or image to a specified path.
Arguments:
url: Instagram post URL.
download_path: Path where the content will be saved.
Logic: It extracts the shortcode from the URL, checks if the post is a video, and downloads it using asynchronous HTTP requests.
get_upload_url()
Purpose: Fetches the URL and hash value for uploading content to the API.
Logic: Makes an HTTP GET request to the API to retrieve the URL and hash required for the upload process.
upload_video(upload_url, video_file_path)
Purpose: Uploads the video to the remote API using the provided URL and video file.
Arguments:
upload_url: URL to upload the video.
video_file_path: Local path of the video file to upload.
create_post(title, hash_value, category_id)
Purpose: Creates a new post with the uploaded video using the provided hash value.
Arguments:
title: Title of the post.
hash_value: Hash from the uploaded content.
category_id: Category for the post.
delete_local_file(file_path)
Purpose: Deletes the local video file after it has been uploaded to avoid clutter.
process_video_file(video_file_path)
Purpose: Coordinates the entire process for a single video: upload, post creation, and file deletion.
process_multiple_videos(video_urls, download_path)
Purpose: Handles the process of downloading multiple Instagram videos concurrently and uploading them after processing.
VideoFileHandler(FileSystemEventHandler)
Purpose: Monitors the specified folder for new .mp4 files and triggers the processing function when a new file is detected.
README Quality
The README should contain the following sections:

1. Project Description
A concise explanation of what the project does, its purpose, and its main features.
2. Installation Instructions
Detailed steps on how to set up the project, install dependencies, and configure necessary tokens and environment variables.
3. Usage Instructions
How to run the bot and provide Instagram URLs.
How the bot processes new video files in the monitored directory.
4. Code Explanation
High-level overview of the main functions and classes in the code, what they do, and how they fit into the larger workflow.
5. Contributing
How others can contribute to the project (e.g., issues, pull requests).
6. License
Information about the project's license.
License
This project is licensed under the MIT License - see the LICENSE file for details.

