# test_downloader.py
from youtube_comment_downloader import YoutubeCommentDownloader

YOUR_YOUTUBE_URL = "https://www.youtube.com/watch?v=Fbv6-50S1lc&list=RDFbv6-50S1lc&start_radio=1" # Example: Rick Astley's "Never Gonna Give You Up" has millions
# Or use the URL you were trying: "https://www.youtube.com/watch?v=rW0eeTXas4k&t=4s"

downloader = YoutubeCommentDownloader()
try:
    print(f"Attempting to download comments from: {YOUR_YOUTUBE_URL}")
    comments_generator = downloader.get_comments_from_url(YOUR_YOUTUBE_URL, language='en')

    comment_count = 0
    for comment in comments_generator:
        print(f"Comment: {comment['text'][:70]}...")
        comment_count += 1
        if comment_count >= 5: # Just print 5 comments to quickly verify
            break

    if comment_count == 0:
        print("No comments returned by the downloader for this URL.")
    else:
        print(f"Successfully downloaded {comment_count} comments (displaying first 5).")

except Exception as e:
    print(f"An error occurred while downloading comments: {e}")