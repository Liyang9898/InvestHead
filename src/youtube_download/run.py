from youtube_download.youtube_download_lib import download_youtube

url = 'https://www.youtube.com/watch?v=7wPBa4lryY4'

output_folder = 'C:/youtube_download/air/'
audio_only= False
download_youtube(url, output_folder, audio_only)