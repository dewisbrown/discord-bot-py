from pytube import YouTube

yt = YouTube('https://www.youtube.com/watch?v=vFo7hQDtjWc')

audio_stream = yt.streams.filter(only_audio=True).first()

audio_stream.download(output_path='downloads')
