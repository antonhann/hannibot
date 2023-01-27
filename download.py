from pytube import YouTube
import os
from pathlib import Path
import sys


def youtube2mp3 (url,outdir ="/mnt/c/Users/anton/local files"):
    # url input from user
    
    yt = YouTube(url)
    video = yt.streams.filter(abr='160kbps').last()
    out_file = video.download(output_path=outdir)
    base, ext = os.path.splitext(out_file)
    new_file = Path(f'{base}.mp3')
    os.rename(out_file, new_file)
    ##@ Check success of download
    if new_file.exists():
        return (f'{yt.title} has been successfully downloaded.')
        
    else:
        return(f'ERROR: {yt.title}could not be downloaded!')

# path_to_download_folder = str(os.path.join(Path.home(), "Downloads"))
# print(Path.cwd())
# url = "www.youtube.com/watch?v=6TIO66S_hHo"
# youtube2mp3(url)
