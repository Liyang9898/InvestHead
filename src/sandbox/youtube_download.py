import pytube

url = 'https://www.youtube.com/watch?v=ncqcfDukrPw'

youtube = pytube.YouTube(url)
video = youtube.streams.first()
video.download('D:/youtube_download')

# https://www.studytonight.com/post/pytube-to-download-youtube-videos-with-python