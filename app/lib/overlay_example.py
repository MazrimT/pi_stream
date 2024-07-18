from PIL import Image as im
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput
import numpy as np
from picamera2 import Picamera2, MappedArray
import time
import threading

# sets the width and height for picture both from the camera and is used to downscale overlays if needed
# replace with arguments or where-ever you want to pick up resolution from
WIDTH = 1920
HEIGHT = 1080

# overlay variables
OVERLAY_IMAGE_PATH = "overlay.png"
OVERLAY_IMAGE = None
OVERLAY_ALPHA = None
OVERLAY_UPDATE_DELAY = 10
STOP_OVERLAY_UPDATE_THREAD = False


def main():
    # set main to use the global variable
    global STOP_OVERLAY_UPDATE_THREAD

    # set up the thread that will update the image if it changes
    # if you don't want it as a thread just run the function once and remove its while loop
    update_overlay_thread = threading.Thread(target=update_overlay)
    update_overlay_thread.start()

    # set up picamera with the requested width and height
    picam2 = Picamera2()
    picam2.video_configuration.size = (WIDTH, HEIGHT)

    # add the overlay
    picam2.pre_callback = apply_overlay

    # only tested with H264Encoder, other might work just as well
    encoder = H264Encoder()

    # change to whatever output you want
    output = FfmpegOutput('overlay_video.mp4')

    # start recording for 10 seconds
    picam2.start_recording(encoder, output)
    time.sleep(10)

    # shut everything down nicely
    print("Stopping recording, please wait")
    picam2.stop_recording()
    picam2.close()
    print("Stopping the overlay update thread, please wait")
    STOP_OVERLAY_UPDATE_THREAD = True
    update_overlay_thread.join()


def apply_overlay(request):
    """Uses PIL to update the image.
    After a lot of testing this was the fastest way to add an overlay.
    Even with converting to PIL and back again this is much faster than methods where you update each color channel in a loop.
    Since this has to happen for every single frame this makes a huge difference.
    """
    with MappedArray(request, "main") as m:

        # turns the frame into an PIL image
        image = im.fromarray(m.array)

        # pastes the overlay ontop of the image
        image.paste(OVERLAY_IMAGE, (0, 0), OVERLAY_ALPHA)

        # turns the image back into a frame array
        m.array[:] = np.asarray(image)

def update_overlay():
    """This function turns the overlay png into a PIL image and a PIL image alpha channel
    Reason to do this in a separate function is that these values do not change as long as the image does not change.
    Doing this for each frame would slow down the processing so much it would not be able to record in realtime.

    """
    global OVERLAY_IMAGE
    global OVERLAY_ALPHA

    while True:

        if STOP_OVERLAY_UPDATE_THREAD:
            break

        overlay_image = im.open(OVERLAY_IMAGE_PATH).convert('RGBA')

        # check if we need to resize at all, if not skip it
        if overlay_image.width > WIDTH or overlay_image.height > HEIGHT:

            overlay_width = WIDTH if overlay_image.width > WIDTH else overlay_image.width
            overlay_height = HEIGHT if overlay_image.height > HEIGHT else overlay_image.height
            overlay_image = overlay_image.resize(overlay_width, overlay_height)

        # set both at the same time so we don't try to apply missmatching values if the image changes
        OVERLAY_IMAGE, OVERLAY_ALPHA = overlay_image, overlay_image.getchannel('A')

        time.sleep(OVERLAY_UPDATE_DELAY)

if __name__ == "__main__":

    main()
