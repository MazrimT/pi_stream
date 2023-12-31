import time
import os
import argparse


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

    while True:            
        print(f'{os.getpid()} - streaming to {stream_url}')
        time.sleep(5)
    
    
    
    
    
    
if __name__ == '__main__':

    args = get_args()
    
    streaming_service = args.streaming_service if args.streaming_service else 'youtube'
    stream_key = args.stream_key if args.stream_key else 'xxxxxxxx'
        
    main(streaming_service, stream_key)