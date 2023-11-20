import os
from pytube import YouTube
from pytube import Search

def download(url, request_author):
    '''Downloads YouTube video and returns YouTube video data.'''
    try:
        if is_url(url): # check to see if user input from play command is a youtube url
            yt = YouTube(url)
        else:
            yt = Search(url).results[0] # first result of search query

        audio_stream = yt.streams.filter(only_audio=True).first()
        output_path = os.path.join(os.path.dirname(__file__), 'downloads')
        file_path = audio_stream.download(output_path=output_path)

        return {
            'song_name': yt.title, 
            'song_duration': format_time(yt.length), 
            'request_author': request_author, 
            'thumbnail_url': yt.thumbnail_url, 
            'file_path': file_path
        }
    except Exception as ex:
        print(str(ex))


def format_time(seconds):
    '''Formats total seconds to %M:%S format.'''
    minutes, seconds = divmod(seconds, 60)
    return f'{minutes}:{seconds:02d}'


def delete(file_path):
    '''Deletes audio file from downloads directory.'''
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            print(f'Succesfully deleted {file_path}')
        except OSError as error:
            print(f'Error deleting file: {error}')
    else:
        print('The file path does not exist.')
        print(file_path)


def is_url(user_input: str) -> bool:
    '''Checks if input string is a YouTube url.'''
    if 'https://www.youtube.com/' in user_input:
        return True
    return False
