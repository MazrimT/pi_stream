import requests
from pathlib import Path
from app.lib.config import Config
import shutil

def download_overlay():

    current_path = Path(__file__).parent
    image_path = current_path.joinpath("../static/images").resolve()
    default_overlay_path = image_path.joinpath("default_overlay.png")
    current_overlay_path = image_path.joinpath("current_overlay.png")

    config = Config()
    overlay_url = config.overlay_url

    if config.overlay == 'on':
        if overlay_url:

            r = requests.get(overlay_url, stream=True)
            if r.status_code == 200:
                with open(current_overlay_path, 'wb') as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)

                print(f"Overlay file updated from {overlay_url}")

        else:
            # we make sure the current_overlay = default overlay
            shutil.copyfile(src=default_overlay_path, dest=current_overlay_path)

if __name__ == '__main__':

    download_overlay()