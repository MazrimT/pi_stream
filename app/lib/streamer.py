import time
import argparse
from picamera2.encoders import MJPEGEncoder, H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2, MappedArray
import cv2
import time
import os


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
    
    parser.add_argument(
        '--resolution',
        required=False,
        type=str,
        help="Streaming resolution, default 1280x720",
        default="1280x720"
    )

    return parser.parse_args()

def apply_overlay(request):
    
    global OVERLAY_UPDATE_TIME
    global OVERLAY_IMAGE
    global OVERLAY_WIDTH
    global OVERLAY_HEIGHT 
    global OVERLAY_COLOR
    global OVERLAY_ALPHA
    
    if time.time() - OVERLAY_UPDATE_TIME > 10:
        OVERLAY_IMAGE, OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_COLOR, OVERLAY_ALPHA = get_overlay()
        OVERLAY_UPDATE_TIME = time.time()
    
    with MappedArray(request, "main") as m:
        
        frame = m.array
        # Overlay the image
        for c in range(0, 3):
            frame[0:OVERLAY_HEIGHT, 0:OVERLAY_WIDTH, c] = (OVERLAY_ALPHA * OVERLAY_COLOR[:, :, c] +
                                (1 - OVERLAY_ALPHA) * frame[0:OVERLAY_HEIGHT, 0:OVERLAY_WIDTH, c])
            
            
def get_overlay():
    
    overlay_image = cv2.imread(OVERLAY_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
    overlay_height, overlay_width = overlay_image.shape[:2] # for some reason height first in the array
    resize_overaly = False
    if overlay_width > WIDTH:
        overlay_width = WIDTH
        resize_overaly = True
    
    if overlay_height > HEIGHT:
        overlay_height = HEIGHT
        resize_overaly = True
        
    if resize_overaly:
        overlay_image = cv2.resize(overlay_image, (overlay_width, overlay_height))

    overlay_color = overlay_image[:, :, :3]
    overlay_alpha = overlay_image[:, :, 3] / 255.0            
    if overlay_image.shape[2] == 4:  # If the image has 4 channels
        overlay_color = cv2.cvtColor(overlay_color, cv2.COLOR_BGR2RGB)     
        
    return overlay_image, overlay_width, overlay_height, overlay_color, overlay_alpha
     


                
def main():
    
    if STREAMING_SERVICE == "twitch":
        stream_url = f"rtmp://live.twitch.tv/app/{STREAM_KEY}"
    elif STREAMING_SERVICE == "youtube":
        stream_url = f"rtmp://a.rtmp.youtube.com/live2/{STREAM_KEY}"

    # resource for some of this:
    # https://trac.ffmpeg.org/wiki/EncodingForStreamingSites
    ffmpeg_command = [
        '-framerate 30',
        '-g 60',
        f'-s {WIDTH}x{HEIGHT}',
        '-c:v libx264',
        '-b:v 10000k',
        '-preset veryfast',
        '-maxrate 10000k',
        '-bufsize 960k',
        '-threads 8',
        '-ignore_unknown',
        '-sn',
        '-f flv',
        stream_url,
    ]
    
    ffmpeg_string = ' '.join(ffmpeg_command)

    picam2 = Picamera2()
    video_config = picam2.create_video_configuration(main={"size": (WIDTH, HEIGHT)})
    video_config["buffer_count"] = 6
    picam2.configure(video_config)
    
    picam2.pre_callback = apply_overlay
    
    encoder = H264Encoder(bitrate=10000000)
    output = FfmpegOutput(ffmpeg_string, audio=True)
    
    picam2.start_recording(encoder, output)

   
    
    
        
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Handle any cleanup here
        pass
    finally:
        picam2.stop_recording()
        picam2.close()


if __name__ == '__main__':

    args = get_args()

    STREAMING_SERVICE = args.streaming_service if args.streaming_service else 'youtube'
    STREAM_KEY = args.stream_key if args.stream_key else 'xxxxxxxx'
    WIDTH = int(args.resolution.split('x')[0])
    HEIGHT = int(args.resolution.split('x')[1])

    OVERLAY_IMAGE_PATH = os.path.dirname(os.path.realpath(__file__)) + "/../static/images/overlay.png"
    
    OVERLAY_IMAGE, OVERLAY_WIDTH, OVERLAY_HEIGHT, OVERLAY_COLOR, OVERLAY_ALPHA = get_overlay()
    OVERLAY_UPDATE_TIME = time.time()
    
    main()
