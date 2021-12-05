import pytube

url = 'https://www.youtube.com/watch?v=byluKMLHGyY'

youtube = pytube.YouTube(url)
video = youtube.streams.first()
video.download('D:/youtube_download')