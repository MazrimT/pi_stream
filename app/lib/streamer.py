import time
import os
import argparse
import ffmpeg



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
        help='The secret sauce key to connect to Youtube or Twitch with'
    )
    parser.add_argument(
        '--title',
        required=False,
        type=str,
        help='The title of the stream on youtube/twitch'
    )
    
    return parser.parse_args()

        
        
def main(streaming_service, stream_key):


    if streaming_service == "twitch":
        stream_url = f"rtmps://live.twitch.tv/app/{stream_key}"
    elif streaming_service == "youtube":
        stream_url = f"rtmps://a.rtmp.youtube.com/live2/{stream_key}"

    # set up the stream
    video_input = ffmpeg.input(
        filename='/dev/video0',
        input_format='mjpeg',
    )
    audio_input = ffmpeg.input(
        filename='anullsrc=sample_rate=48000:channel_layout=mono',
        f='lavfi',
    )
    stream = ffmpeg.output(
        audio_input,
        video_input, 
        filename=stream_url, 
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
        dn=None,
    )
    ffmpeg.run(stream, overwrite_output=True)




    
    
if __name__ == '__main__':

    args = get_args()
    
    streaming_service = args.streaming_service if args.streaming_service else 'youtube'
    stream_key = args.stream_key if args.stream_key else 'xxxxxxxx'
        
    main(streaming_service, stream_key)