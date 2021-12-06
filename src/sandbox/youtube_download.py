import pytube

url = 'https://www.youtube.com/watch?v=i1qesKr8gSg&list=PL2DJkyutq79tEVR5kCzU-BeL35E5P8UNV&index=90'

youtube = pytube.YouTube(url)
video = youtube.streams.first()
video.download('D:/youtube_download')

# https://www.studytonight.com/post/pytube-to-download-youtube-videos-with-python