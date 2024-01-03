import time
import os
import argparse
from picamera2.encoders import H264Encoder#, MJPEGEncoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2

def get_args():
    parser = argparse.ArgumentParser(description="Parse arguments")
    parser.add_argument(
        '--streaming_service',
        required=False,
        type=str,
        help='The service to stream to, Youtube or Twitch'
    )
    parser.add_argument(
        '--stream_key',
        required=False,
        type=str,
        help='The secret key to connect to Youtube or Twitch with'
    )
    
    return parser.parse_args()


def main(streaming_service, stream_key):


    if streaming_service == "twitch":
        stream_url = f"rtmp://live.twitch.tv/app/{stream_key}"
    elif streaming_service == "youtube":
        stream_url = f"rtmp://a.rtmp.youtube.com/live2/{stream_key}"

    # resource for some of this:
    # https://trac.ffmpeg.org/wiki/EncodingForStreamingSites
    ffmpeg_command = [
        '-framerate 30',
        '-g 60',
        '-s 1920x1080',
        '-c:v libx264',
        '-b:v 4500k',
        '-preset veryfast',
        '-maxrate 5000k',
        '-bufsize 6000k',
        '-threads 8',
        '-ignore_unknown',
        '-sn',
        '-f flv',
        stream_url,
    ]
    ffmpeg_string = ' '.join(ffmpeg_command)

    print(ffmpeg_string)

    picam2 = Picamera2()
    video_config = picam2.create_video_configuration()
    picam2.configure(video_config)
    encoder = H264Encoder()
    output = FfmpegOutput(ffmpeg_string, audio=True, audio_bitrate=128000, audio_codec = "aac")

    picam2.start_recording(output=output, encoder=encoder)

    while True:
       time.sleep(100)
    picam2.stop_recording()
    


if __name__ == '__main__':

    args = get_args()

    streaming_service = args.streaming_service if args.streaming_service else 'youtube'
    stream_key = args.stream_key if args.stream_key else 'xxxxxxxx'

    main(streaming_service, stream_key)
