import youtube_dl
import os

output_dir = 'downloads'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def download_progress_hook(d):
    if d['status'] == 'finished':
        print('Download completed!')
    elif d['status'] == 'downloading':
        print(f'Downloaded {d["_percent_str"]} of the video.')

ydl_opts = {
    'format': 'best',
    'outtmpl': f'{output_dir}/$(title)s.%(ext)s',
    'verbos': True,
    'progress_hooks': [download_progress_hook],
    'force_generic_extractor': True,
}

url = 'https://www.youtube.com/watch?v=9u36BKakKyw'

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])