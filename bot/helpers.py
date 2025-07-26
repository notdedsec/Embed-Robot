import os
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

import requests
from yt_dlp import YoutubeDL

YTDL_WORKERS = os.getenv('YTDL_WORKERS').split(',')
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
    if YTDL_WORKERS and any(x in url for x in ['instagram.com', 'tiktok.com']):
        for _ in range(len(YTDL_WORKERS)):
            worker = YTDL_WORKERS[0]
            YTDL_WORKERS.append(YTDL_WORKERS.pop(0))
            
            try:
                return requests.get(worker, params={'url': url}).json()
            except:
                continue

    try:
        return ytdl.extract_info(url, download=False)
    except:
        return ytdl_fallback.extract_info(url, download=False)


def clean_url(url: str) -> str:
    parsed_url = urlparse(url)
    query_params = parse_qsl(parsed_url.query)

    filtered_params = [(k, v) for k, v in query_params if k == 'v']

    clean_query = urlencode(filtered_params)
    clean_url = urlunparse(parsed_url._replace(query=clean_query))

    return clean_url
