"""
This file contains all the code for interacting with the YouTube video download related stuff
"""
import pytube


def search(url):
    video = pytube.YouTube(url=url)
    streams = video.streams

    return {
        "streams": [stream for stream in streams
                    if stream.mime_type == "video/mp4"
                    or stream.mime_type == "audio/mp4"
                    or stream.mime_type == "audio/mp3"
                    ],
        "thumbnail_url": video.thumbnail_url,
        "title": video.title,
        "originalStream": streams
    }
