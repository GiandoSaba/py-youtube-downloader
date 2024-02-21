from pytube import YouTube
import shutil
import sys


def size_format(b):
    if b < 1000:
              return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'

def display_progress_bar(
    bytes_received: int, filesize: int, ch: str = "█", scale: float = 0.55
) -> None:
    columns = shutil.get_terminal_size().columns
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    progress_bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)

    text = f" ↳ |{progress_bar}| {percent}% ~ {size_format(bytes_received)}\r"
    sys.stdout.write(text)
    sys.stdout.flush()

def progress(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)

    
def download_youtube(url):

    yt = YouTube(url, on_progress_callback=progress)

    print(f'\nDownloading: {yt.title} ~ viewed {yt.views} times.')

    yt.streams.first().download('downloads')
    
    file_size = size_format(yt.streams.first().filesize)

    print(f'\nFinished downloading:  {yt.title}, total size: {file_size}')

if __name__ == '__main__':
    url = input('Enter the URL of the video: ')
    download_youtube(url)
