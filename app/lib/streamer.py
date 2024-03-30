import time
import argparse
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2, MappedArray
import cv2
import time
import os
from libcamera import controls
import threading
import numpy as np

def get_args():
    parser = argparse.ArgumentParser(description="Parse arguments")

    parser.add_argument(
        "--streaming_service",
        required=False,
        type=str,
        help="The service to stream to, uoutube or twitch, default youtube",
        default="youtube",
    )

    parser.add_argument(
        "--stream_key",
        required=False,
        type=str,
        help="The secret key to connect to Youtube or Twitch with",
    )

    parser.add_argument(
        "--resolution",
        required=False,
        type=str,
        help="Streaming resolution, default 1920x1080",
        default="1920x1080",
    )

    parser.add_argument(
        "--bitrate",
        required=False,
        type=str,
        help="Stream and video bitrate bps, default 6800k",
        default="6800k",
    )

    parser.add_argument(
        "--framerate",
        required=False,
        type=str,
        help="Streaming framerate, default 30",
        default="30",
    )

    parser.add_argument(
        "--overlay",
        required=False,
        type=str,
        help="if to add the png overlay on/off",
        default="on",
    )

    return parser.parse_args()


def apply_overlay(request):

    with MappedArray(request, "main") as m:

        frame = m.array

        # this is a bit complicated and unfortunatly the most efficient way to do it.
        # The first three color channels in the frame needs to be updated with info from the overlay taking into account the transparency/alpha layer from the overlay.
        # doing this as comprehension tuple is more efficient than a doing it in a normal for loop and since we need to do this for every frame all optimization possible is needed.
        # at the end np.stack(tuple(), axis=1) turns it all back into the same format as a frame.
        frame[0:OVERLAY_HEIGHT, 0:OVERLAY_WIDTH, :3] = np.stack(
            tuple(
                (
                    OVERLAY_ALPHA * OVERLAY_IMAGE[:, :, c]
                    + (1 - OVERLAY_ALPHA) * frame[0:OVERLAY_HEIGHT, 0:OVERLAY_WIDTH, c]
                )
                for c in range(0, 3)
            ),
            axis=-1
        )


def update_overlay():

    global OVERLAY_WIDTH
    global OVERLAY_HEIGHT
    global OVERLAY_IMAGE
    global OVERLAY_ALPHA

    while True:

        if STOP_OVERLAY_UPDATE_THREAD:
            break

        # read t he image
        overlay_image = cv2.imread(OVERLAY_IMAGE_PATH, cv2.IMREAD_UNCHANGED)

        # convert to BRGA to match picamera output.
        # This will convert any 3 or 4 color channel image, grayscale might not work
        overlay_image = cv2.cvtColor(overlay_image, cv2.COLOR_RGB2BGRA)

        # for some reason height first in the array
        overlay_height, overlay_width = overlay_image.shape[:2]

        resize_overlay = True if overlay_width > WIDTH or overlay_height > HEIGHT else False
        overlay_width = WIDTH if overlay_width > WIDTH else overlay_width
        overlay_height = HEIGHT if overlay_height > HEIGHT else overlay_height

        if resize_overlay:
            overlay_image = cv2.resize(overlay_image, (overlay_width, overlay_height))

        # break out alpha to separate variable it is needed and more effiient to do once rather than for every frame
        overlay_alpha = overlay_image[:, :, 3] / 255.0

        (
            OVERLAY_WIDTH,
            OVERLAY_HEIGHT,
            OVERLAY_IMAGE,
            OVERLAY_ALPHA,
        ) = (
            overlay_width,
            overlay_height,
            overlay_image,
            overlay_alpha,

        )

        time.sleep(OVERLAY_UPDATE_DELAY)


def main():
    global STOP_OVERLAY_UPDATE_THREAD

    update_overlay_thread = threading.Thread(target=update_overlay)
    update_overlay_thread.start()
    # a short sleep so that the overlay has time to get set
    time.sleep(1)
    if ARGS.streaming_service == "twitch":
        stream_url = f"rtmp://live.twitch.tv/app/{ARGS.stream_key}"
    elif ARGS.streaming_service == "youtube":
        stream_url = f"rtmp://a.rtmp.youtube.com/live2/{ARGS.stream_key}"

    ffmpeg_command = [
        "-threads 4",
        "-c copy",
        "-f flv",
        stream_url,
    ]

    ffmpeg_string = " ".join(ffmpeg_command)

    # set up picam
    picam2 = Picamera2()
    picam2.video_configuration.controls.FrameRate = int(ARGS.framerate)
    picam2.video_configuration.size = (WIDTH, HEIGHT)

    # turns on autofocus if supported
    try:
        picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
    except RuntimeError as e:
        print("Autofocus not supported on this camera")

    if ARGS.overlay == 'on':
        picam2.pre_callback = apply_overlay

    bitrate_int = int(ARGS.bitrate.replace('M', "000000").replace('k', "000"))
    encoder = H264Encoder(bitrate=bitrate_int)

    # with -c copy have to lock the audio_samplerate to 44100, 22050 or 11025, youtube gets sad when it's not 44100
    output = FfmpegOutput(ffmpeg_string, audio=True, audio_samplerate=44100)

    picam2.start_recording(encoder, output)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Safely stopping stream, please wait")
        STOP_OVERLAY_UPDATE_THREAD = True
        update_overlay_thread.join()
        picam2.stop_recording()
        picam2.close()


ARGS = get_args()
WIDTH = int(ARGS.resolution.split("x")[0])
HEIGHT = int(ARGS.resolution.split("x")[1])

# overlay variables
OVERLAY_IMAGE_PATH = (
    os.path.dirname(os.path.realpath(__file__)) + "/../static/images/overlay.png"
)
OVERLAY_WIDTH = None
OVERLAY_HEIGHT = None
OVERLAY_IMAGE = None
OVERLAY_ALPHA = None
OVERLAY_UPDATE_DELAY = 10
STOP_OVERLAY_UPDATE_THREAD = False

if __name__ == "__main__":

    main()
