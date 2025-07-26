import os

import requests
from yt_dlp import YoutubeDL

YTDL_WORKER = os.getenv('YTDL_WORKER')
PO_TOKEN = os.getenv('PO_TOKEN')

COOKIES_BROWSER = os.getenv('COOKIES_BROWSER')
COOKIES_PROFILE = os.getenv('COOKIES_PROFILE')

ytdl = YoutubeDL({
    'format': 'b[filesize<=?10M][filesize_approx<=?10M]',
    'quiet': True,
    'no_color': True,
    'cookiesfrombrowser': (COOKIES_BROWSER, COOKIES_PROFILE),
    'extractor_args': {'youtube': [f'player-client=default,mweb;po_token=mweb.gvs+{PO_TOKEN}']}
})

ytdl_fallback = YoutubeDL({
    'format': 'w',
    'quiet': True,
    'no_color': True,
    'cookiesfrombrowser': (COOKIES_BROWSER, COOKIES_PROFILE),
    'extractor_args': {'youtube': [f'player-client=default,mweb;po_token=mweb.gvs+{PO_TOKEN}']}
})


def get_info(url: str) -> dict:
    if YTDL_WORKER and any(x in url for x in ['instagram.com', 'tiktok.com']):
        return requests.get(YTDL_WORKER, params={'url': url}).json()
    else:
        try:
            return ytdl.extract_info(url, download=False)
        except:
            return ytdl_fallback.extract_info(url, download=False)

