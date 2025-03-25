from yt_dlp import YoutubeDL

ytdl_options = {
    'format': 'b[filesize<=?10M][filesize_approx<=?10M]',
    'quiet': True,
}
ytdl = YoutubeDL(ytdl_options)


def get_info(url: str) -> dict:
    return ytdl.extract_info(url, download=False)
