import asyncio
import os
from time import sleep

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from pytube import YouTube

# pip install git+https://github.com/baxterisme/pytube
from queStorage import storeInQueue


def remove_file(path):
    sleep(120)
    os.remove(f"./cutted/{path}")
    print(f'Removed ./cutted/{path}')
    os.remove(f"./videos/{path}")
    print(f'Removed ./videos/{path}')


@storeInQueue
def cut_video(url, start_time, end_time):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yt = YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download("./videos")
    file_name = yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution').desc().first().default_filename
    ffmpeg_extract_subclip(f"./videos/{file_name}", start_time, end_time, targetname=f"./cutted/{file_name}")

    return file_name
