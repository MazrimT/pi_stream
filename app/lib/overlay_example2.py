import time
import argparse
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
from picamera2 import Picamera2, MappedArray
import time
from libcamera import controls
import threading
import numpy as np
from PIL import Image as im
from pathlib import Path
import sys


HEIGHT = X
WIDTH = Y

def apply_overlay(request):
    """ turns each frame into an image with PIL and, uses PILs paste to put the overlay on it and then converts back to frame.
    The Paste function in PIL is implemented in C, doing this in python is way to slow.
    """
    with MappedArray(request, "main") as m:

        image = im.fromarray(m.array)
        image.paste(OVERLAY_IMAGE, (0, 0), OVERLAY_ALPHA)
        m.array[:] = np.asarray(image)


def update_overlay():
    """ Optional function to update the overlay every X seconds
    """
    global OVERLAY_IMAGE
    global OVERLAY_ALPHA

    while True:

        if STOP_OVERLAY_UPDATE_THREAD:
            break

        overlay_image = im.open(OVERLAY_IMAGE_PATH).convert('RGBA')

        overlay_image = im.open(DEFAULT_OVERLAY_IMAGE_PATH).convert('RGBA')

        if overlay_image.width > WIDTH or overlay_image.height > HEIGHT:
            overlay_width = WIDTH if overlay_image.width > WIDTH else overlay_image.width
            overlay_height = HEIGHT if overlay_image.height > HEIGHT else overlay_image.height
            overlay_image = overlay_image.resize(overlay_width, overlay_height)

        # set both at the same time so we don't try to apply missmatching values if the image changes
        OVERLAY_IMAGE, OVERLAY_ALPHA = overlay_image, overlay_image.getchannel('A')

        time.sleep(OVERLAY_UPDATE_DELAY)


def main():
    #global STOP_OVERLAY_UPDATE_THREAD

    # start the update overlay thread, can be ignored if you don't want to have functionality to change the overlay image
    update_overlay_thread = threading.Thread(target=update_overlay)
    update_overlay_thread.start()

    # a short sleep so that the overlay has time to get set
    time.sleep(1)

    # set up picam
    picam2 = Picamera2()
    picam2.video_configuration.size = (WIDTH, HEIGHT)

    # add overlay
    picam2.pre_callback = apply_overlay


    encoder = H264Encoder(10000000)
    output = FfmpegOutput('output.mp4', audio=True)

    # starting recording
    try:
        picam2.start_recording(encoder, output)
    except Exception as e:
        print(e)
        raise

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        print("Safely stopping stream, please wait")
        picam2.stop_recording()
        picam2.close()
        print("Stopping update thread, please wait")
        STOP_OVERLAY_UPDATE_THREAD = True
        update_overlay_thread.join()



ARGS = get_args()
WIDTH = int(ARGS.resolution.split("x")[0])
HEIGHT = int(ARGS.resolution.split("x")[1])

# overlay variables
OVERLAY_IMAGE_PATH = Path(__file__).parent.parent.joinpath("static/images/current_overlay.png").as_posix()
DEFAULT_OVERLAY_IMAGE_PATH = Path(__file__).parent.parent.joinpath("static/images/default_overlay.png").as_posix()
OVERLAY_IMAGE = None
OVERLAY_ALPHA = None
OVERLAY_UPDATE_DELAY = 10
STOP_OVERLAY_UPDATE_THREAD = False

if __name__ == "__main__":

    main()
