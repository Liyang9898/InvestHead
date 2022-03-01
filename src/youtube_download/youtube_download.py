import pytube
 

def download_youtube(url, output_path, audio_only):
    """
    This function download url content and output to output_path
    if audio_only = True, download audio only, otherwise download video
    quality is default to best
    it also print out all available qualities
    """
    # how to use it: 
    # https://pytube.io/en/latest/user/streams.html#filtering-streams
    # https://stackoverflow.com/questions/65255275/pytube-set-resolution
    youtube = pytube.YouTube(url)
    files = youtube.streams
    
    print('all files')
    for file in files:
        print(file)
        
    best_video = files.get_highest_resolution()
    best_audio = files.get_audio_only()
    
    print('best video')
    print(best_video)
    
    print('best audio')
    print(best_audio)
    if audio_only:
        best_audio.download(output_path)
    else:
        best_video.download(output_path)


url = 'https://www.youtube.com/watch?v=ncqcfDukrPw'
output_folder = 'D:/youtube_download/test/'
audio_only= False
download_youtube(url, output_folder, audio_only)