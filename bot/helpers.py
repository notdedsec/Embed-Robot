import os

import requests
from yt_dlp import YoutubeDL

YTDL_WORKER = os.getenv('YTDL_WORKER')

ytdl_options = {
    'format': 'b[filesize<=?10M][filesize_approx<=?10M]',
    'quiet': True,
}
ytdl = YoutubeDL(ytdl_options)


def get_info(url: str) -> dict:
    if YTDL_WORKER:
        return requests.get(YTDL_WORKER, params={'url': url}).json()
    else:
        return ytdl.extract_info(url, download=False)
