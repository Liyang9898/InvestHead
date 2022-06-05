from youtube_download.youtube_download_lib import download_youtube

url = 'https://www.youtube.com/watch?v=_q5wnUh0D5o&list=RDEMCdI1BKYn9NXZF1MKvyfQvA&start_radio=1'
# url = 'https://www.youtube.com/watch?v=9m8Wshduuhg&list=RD9m8Wshduuhg&start_radio=1'
output_folder = 'C:/youtube_download/air/'
audio_only= True
download_youtube(url, output_folder, audio_only)