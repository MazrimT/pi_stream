from pathlib import Path
from helpers.config import Config
from helpers.logger import Logger
import ffmpeg


def main():

    
    if CONFIG.streaming_service == 'twitch':
        url = f"rtmp://live.twitch.tv/app/{CONFIG.stream_key}"
    elif CONFIG.streaming_service == 'youtube':
        url = f"rtmp://a.rtmp.youtube.com/live2/{CONFIG.stream_key}"

    logger.info(f'using url: {url}')

    video_input = ffmpeg.input(
        filename='/dev/video0',
        input_format='mjpeg',

    )

    audio_input = ffmpeg.input(
        filename='anullsrc',
        f='lavfi',
       # i="anullsrc=r=48000:cl=mono",
       # sample_rate='44100', # 16000
     #   channel_layout='mono',
      #  anullsrc="r=16000:cl=mono",
        acodec="aac", 
        #audio_bitrate="200k"
    )

    video_output = ffmpeg.output(
        video_input, 
        audio_input,
        filename=url, 
        f='flv',
        framerate='30',
        vcodec='libx264',
        preset='ultrafast',
        tune='zerolatency',
        video_size=(1920, 1080),
        video_bitrate='4500k',
        maxrate='5000k',
        bufsize='6000k',
        #threads=4,

    ).global_args('-ignore_unknown').global_args('-dn').global_args('-sn')

    ffmpeg.run(video_output, overwrite_output=True)


if __name__ == '__main__':

    app_path = Path(__file__).parent
    CONFIG = Config(app_path)
    logger = Logger(log_dir=app_path.parent.joinpath('logs'))

    main()