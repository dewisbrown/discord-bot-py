import os
from pytube import YouTube

def download(url, request_author):
    '''Downloads YouTube video and returns YouTube video data.'''
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    output_path = os.path.join(os.path.dirname(__file__), 'downloads')
    audio_stream.download(output_path=output_path)

    return {'song_name': yt.title, 'song_duration': format_time(yt.length), 'request_author': request_author, 'thumbnail_url': yt.thumbnail_url}


def format_time(seconds):
    '''Formats total seconds to %M:%S format.'''
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds:02d}'


def delete(song_title):
    '''Deletes audio file from downloads directory.'''
    os.remove(f'downloads/{song_title}.mp4')
