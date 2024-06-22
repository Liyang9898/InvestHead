from youtube_download.youtube_download_lib import download_youtube

url = 'https://www.youtube.com/watch?v=GbYLZsa696o&list=PLe1YdiKWcqPR-6p2DOrs2wszsDiA1Pxi3&index=2'

output_folder = 'C:/youtube_download/air/'
audio_only= False
download_youtube(url, output_folder, audio_only)