import os
import aiohttp
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import instaloader
import time
import random
from tqdm.asyncio import tqdm  # Import tqdm for async progress bar

# Constants for token and API URLs
API_URL = "https://api.socialverseapp.com"
FLIC_TOKEN = "flic_d437418354877959f742fc5c46169bc8ca1a837e07788d924e109b4d9f96c094"  # Replace with your actual token


async def download_instagram_content(url, download_path):
    """
    Downloads Instagram content (video or image) based on the content type.
    
    Args:
        url (str): The Instagram post URL.
        download_path (str): Path where the content will be saved.
    
    Returns:
        str: Path to the downloaded video file, or None if not a video.
    """
    L = instaloader.Instaloader()

    # Extract shortcode from the URL
    shortcode = url.split("/")[-2]
    print(f"Attempting to download content from shortcode: {shortcode}")

    try:
        # Get the post using the shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)

        # Check if the post is a video
        if post.is_video:
            print(f"Downloading video: {post.video_url}")
            video_url = post.video_url

            # Send GET request to the video URL
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url) as video_response:
                    if video_response.status == 200:
                        video_filename = os.path.join(download_path, f"{shortcode}.mp4")

                        # Get total size of the file for progress bar
                        total_size = int(video_response.headers.get('Content-Length', 0))
                        pbar = tqdm(total=total_size, unit='B', unit_scale=True, desc=f"Downloading {shortcode}.mp4")

                        # Save the video file
                        with open(video_filename, "wb") as video_file:
                            while chunk := await video_response.content.read(1024):
                                video_file.write(chunk)
                                pbar.update(len(chunk))  # Update progress bar

                        pbar.close()
                        print(f"Video downloaded successfully: {video_filename}")
                        return video_filename
                    else:
                        print(f"Failed to download video. Status code: {video_response.status}")
                        return None
        else:
            print("This post is not a video, it is an image.")
            return None

    except Exception as e:
        print(f"Failed to download content: {e}")
        return None


async def get_upload_url():
    """
    Gets the upload URL and hash value from the API for uploading content.
    
    Returns:
        tuple: (upload_url, hash_value) if successful, else (None, None).
    """
    url = f"{API_URL}/posts/generate-upload-url"
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_data = await response.json()

            if response.status == 200:
                return response_data['url'], response_data['hash']
            else:
                print(f"Error getting upload URL: {response_data}")
                return None, None


async def upload_video(upload_url, video_file_path):
    """
    Uploads the video to the API.
    
    Args:
        upload_url (str): URL to upload the video.
        video_file_path (str): Path to the local video file to be uploaded.
    """
    try:
        async with aiohttp.ClientSession() as session:
            with open(video_file_path, 'rb') as video_file:
                response = await session.put(upload_url, data=video_file)

            if response.status == 200:
                print("Video uploaded successfully.")
            else:
                print(f"Failed to upload video. Status code: {response.status}")
                print(await response.text())  # For more error details
    except FileNotFoundError:
        print(f"File not found: {video_file_path}")
    except Exception as e:
        print(f"An error occurred during video upload: {e}")


async def create_post(title, hash_value, category_id):
    """
    Creates a post with the uploaded video.
    
    Args:
        title (str): The title of the post.
        hash_value (str): The hash value from the upload.
        category_id (int): The category ID for the post.
    """
    url = f"{API_URL}/posts"
    headers = {
        "Flic-Token": FLIC_TOKEN,
        "Content-Type": "application/json"
    }

    body = {
        "title": title,
        "hash": hash_value,
        "is_available_in_public_feed": False,
        "category_id": category_id
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body, headers=headers) as response:
            if response.status == 200:
                print("Post created successfully.")
            else:
                print(f"Failed to create post. Status code: {response.status}")
                print(await response.text())  # For more error details


def delete_local_file(file_path):
    """
    Deletes a local file.
    
    Args:
        file_path (str): The path to the file to be deleted.
    """
    try:
        os.remove(file_path)
        print(f"Local file deleted: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {e}")


async def process_video_file(video_file_path):
    """
    Processes a video file by uploading it and creating a post.
    
    Args:
        video_file_path (str): The path to the local video file.
    """
    # Step 1: Get upload URL and hash for uploading
    upload_url, video_hash = await get_upload_url()

    if upload_url and video_hash:
        # Step 2: Upload the video to the API
        await upload_video(upload_url, video_file_path)

        # Step 3: Create the post with the uploaded video
        title = "My Test"
        category_id = 25  # Example category ID
        await create_post(title, video_hash, category_id)

        # Step 4: Delete the local video file after upload
        delete_local_file(video_file_path)


async def process_multiple_videos(video_urls, download_path):
    """
    Downloads and processes multiple Instagram videos concurrently.
    
    Args:
        video_urls (list): List of Instagram video URLs.
        download_path (str): Path where videos will be saved.
    """
    tasks = [download_instagram_content(url, download_path) for url in video_urls]
    video_file_paths = await asyncio.gather(*tasks)

    # Process each downloaded video
    for video_file_path in video_file_paths:
        if video_file_path:
            await process_video_file(video_file_path)


class VideoFileHandler(FileSystemEventHandler):
    """
    Watches the directory for new video files and processes them.
    """
    async def on_created(self, event):
        if event.src_path.endswith('.mp4'):
            print(f"New video file detected: {event.src_path}")
            await process_video_file(event.src_path)


# Main workflow
if __name__ == "__main__":
    # For demonstration, a list of Instagram URLs (can be fetched dynamically in a more complete solution)
    instagram_video_urls = [
        "https://www.instagram.com/p/B-65ymYAUoo/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA==",
        "https://www.instagram.com/p/B9gxxoDAXw9/?utm_source=ig_web_copy_link&igsh=MzRlODBiNWFlZA=="
        # Add more URLs as needed
    ]
    download_path = r"C:\Users\csrid\video-bot\videos"  # Directory where the content will be saved

    # Start the async process to download and process the videos
    asyncio.run(process_multiple_videos(instagram_video_urls, download_path))

    # Step 6: Monitor the /videos directory for new .mp4 files
    event_handler = VideoFileHandler()
    observer = Observer()
    observer.schedule(event_handler, path=download_path, recursive=False)
    observer.start()

    try:
        print("Monitoring /videos directory for new files...")
        while True:
            time.sleep(1)  # Keep alive
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        observer.stop()
    observer.join()
