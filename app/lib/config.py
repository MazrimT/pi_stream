from pathlib import Path
import json
import tomlkit


class Config(object):
    def __init__(self, app_path):
        self.app_path = app_path
        self.config_file = f"{app_path}/config/config.toml"

        self._data = self._load_config()

        # Properties not written to file and always defaulted on start
        self.streaming = "off"
        self.stream_process_id = None

        # possible options for settings
        self.options = {
            "streaming_services": ["youtube", "twitch"],
            "resolutions": ["1920x1080", "1280x720", "640x480"],
            "bitrates": ["1000k", "1500k", "2500k", "3000k", "4000k", "4500k", "5000k", "6000k", "6800k", "7500k", "8M", "12M", "16M", "24M",  "45M", "68M", "160M", "240M"],
            "framerates": ["15", "30", "60"],
            "overlay": ["on", "off"],
            "threads": ["1", "2", "3", "4"]
        }

    def __str__(self):
        return json.dumps(self._data)

    def _load_config(self):
        with open(self.config_file, "rt", encoding="utf-8") as f:
            return tomlkit.load(f)

    def _write_config(self):
        # also update the config file
        with open(self.config_file, mode="wt", encoding="utf-8") as fp:
            tomlkit.dump(self._data, fp)

    # Properties

    ## Stream Key
    @property
    def stream_key(self):
        return self._data["stream_key"]

    @stream_key.setter
    def stream_key(self, value):
        self._data["stream_key"] = value
        self._write_config()

    ## Streaming Service
    @property
    def streaming_service(self):
        return self._data["streaming_service"]

    @streaming_service.setter
    def streaming_service(self, value):
        self._data["streaming_service"] = value
        self._write_config()

    ## Resolution
    @property
    def resolution(self):
        return self._data["resolution"]

    @resolution.setter
    def resolution(self, value):
        self._data["resolution"] = value
        self._write_config()

    ## Framerate
    @property
    def framerate(self):
        return self._data["framerate"]

    @framerate.setter
    def framerate(self, value):
        self._data["framerate"] = value
        self._write_config()

    ## Bitrate
    @property
    def bitrate(self):
        return self._data["bitrate"]

    @bitrate.setter
    def bitrate(self, value):
        self._data["bitrate"] = value
        self._write_config()

    ## Threads
    @property
    def threads(self):
        return self._data["threads"]

    @threads.setter
    def threads(self, value):
        self._data["threads"] = value
        self._write_config()

    ## Overlay
    @property
    def overlay(self):
        return self._data["overlay"]

    @overlay.setter
    def overlay(self, value):
        self._data["overlay"] = value
        self._write_config()

    ## Overlay URL
    @property
    def overlay_url(self):
        return self._data["overlay_url"]

    @overlay_url.setter
    def overlay_url(self, value):
        self._data["overlay_url"] = value
        self._write_config()


if __name__ == "__main__":
    app_path = Path(__file__).parent.parent.as_posix()

    config = Config(app_path=app_path)
    print(config)
