from youtube_download.youtube_download_lib import download_youtube

url = 'https://www.youtube.com/watch?v=Ijebqy97DdA&list=PLqy3Di5Y4p1puImnUjR2o7eliuply77A9&index=1'

output_folder = 'C:/youtube_download/air/'
audio_only= False
download_youtube(url, output_folder, audio_only)