from pathlib import Path
from helpers.config import Config
import ffmpeg


def main():

    
    if CONFIG.streaming_service == 'twitch':
        url = f"rtmp://live.twitch.tv/app/{CONFIG.stream_key}"
    elif CONFIG.streaming_service == 'youtube':
        url = f"rtmp://a.rtmp.youtube.com/live2/{CONFIG.stream_key}"

    video_input = ffmpeg.input(
        filename='/dev/video0',
        input_format='mjpeg'
    )


    video_output = ffmpeg.output(
        video_input, 
        filename=url, 
        f='flv',
        framerate='30',
        vcodec='libx264',
        preset='ultrafast',
        tune='zerolatency',
        video_size=(1920, 1080),
        video_bitrate='1984k',
        maxrate='5000k',
        bufsize='6000k'
    )

    ffmpeg.run(video_output, overwrite_output=True)


if __name__ == '__main__':

    app_path = Path(__file__).parent
    CONFIG = Config(app_path)


    main()