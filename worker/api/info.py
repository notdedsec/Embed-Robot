import json
from http.server import BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

import yt_dlp


def extract_video_info(url):
    ytdl_options = {
        'format': 'b[filesize<=?10M][filesize_approx<=?10M]',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ytdl_options) as ytdl:
        info = ytdl.extract_info(url, download=False)
        return dict(info)


class handler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json_response(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, message, status_code=400):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps({"error": message}).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        try:
            parsed_path = urlparse(self.path)
            params = parse_qs(parsed_path.query)

            if 'url' not in params:
                self._send_error("Missing 'url' parameter")
                return

            url = params['url'][0]

            try:
                info = extract_video_info(url)
                self._send_json_response(info)
            except Exception as e:
                self._send_error(f"Failed to extract video info: {str(e)}", 500)

        except Exception as e:
            self._send_error(f"Server error: {str(e)}", 500)
