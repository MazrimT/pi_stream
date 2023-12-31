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

    try:
        video_input = ffmpeg.input(
            filename='/dev/video0',
            input_format='mjpeg',

        )
    except Exception as e:
        logger.error("error setting up video input: %s", e)

    try:
        audio_input = ffmpeg.input(
            filename='anullsrc=sample_rate=48000:channel_layout=mono',
            f='lavfi',
        )
    except Exception as e:
        logger.error("error setting up audio input: %s", e)


    try:
        stream = ffmpeg.output(
            audio_input,
            video_input, 
            filename=url, 
            f='flv',
            framerate='30',
            vcodec='libx264',
            acodec="aac", 
            preset='ultrafast',
            tune='zerolatency',
            video_size=(1920, 1080),
            video_bitrate='4500k',
            audio_bitrate="128k",
            maxrate='5000k',
            bufsize='6000k',
            threads=8,
            ignore_unknown=None,
            sn=None,
            dn=None

        )
    except Exception as e:
        logger.error("error setting up stream output: %s", e)

    try:
        ffmpeg.run(stream, overwrite_output=True)
    except Exception as e:
        logger.error("error running the stream: %s", e)

if __name__ == '__main__':

    app_path = Path(__file__).parent
    CONFIG = Config(app_path)
    logger = Logger(log_dir=app_path.parent.joinpath('logs'))

    main()