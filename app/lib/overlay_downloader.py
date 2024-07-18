import requests
from pathlib import Path
from app.lib.config import Config
import shutil

def download_overlay():

    current_path = Path(__file__).parent
    image_path = current_path.parent.joinpath("static/images")
    default_overlay_path = image_path.joinpath("default_overlay.png")
    current_overlay_path = image_path.joinpath("current_overlay.png")

    config = Config()
    overlay_url = config.overlay_url

    if config.overlay == 'on':
        if overlay_url:

            try:
                r = requests.get(overlay_url, stream=True)
                if r.status_code == 200:
                    with open(current_overlay_path, 'wb') as f:
                        r.raw.decode_content = True
                        shutil.copyfileobj(r.raw, f)

                    print(f"Overlay file updated from {overlay_url}")
            except Exception as e:
                print(f"Could not download and save image: {e}")
                print("Will use default image instead")
                shutil.copyfile(src=default_overlay_path, dst=current_overlay_path)

        else:
            # we make sure the current_overlay = default overlay
            shutil.copyfile(src=default_overlay_path, dst=current_overlay_path)

if __name__ == '__main__':

    download_overlay()