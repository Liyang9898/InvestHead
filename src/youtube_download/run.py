from youtube_download.youtube_download_lib import download_youtube

url = 'https://www.youtube.com/watch?v=yGKpdyxtqYo&list=RDCMUC9aLKQEC95YCMKTwfYY4t3g&index=4'

output_folder = 'C:/youtube_download/air/'
audio_only= False
download_youtube(url, output_folder, audio_only)