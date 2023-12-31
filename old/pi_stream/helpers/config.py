from pathlib import Path
import json
import tomlkit


class Config(object):

    def __init__(self, app_path):
        self.app_path = app_path
        self.config_file = f"{app_path}/config/config.toml"
        self.config = self.read_config()

    def __str__(self):
        return json.dumps({
            "app_path": self.app_path.as_posix(),
            "config": self.read_config(),
        })

    
    def read_config(self):

        with open(self.config_file, 'rt', encoding='utf-8') as f:
            return tomlkit.load(f)

    def update_config(self):

        # also update the config file
        with open(self.config_file, mode="wt", encoding="utf-8") as fp:
            tomlkit.dump(self.config, fp)


    # Secrets
    ## Stream Key
    @property
    def stream_key(self):
        return self.config['secrets']['stream_key']

    @stream_key.setter
    def stream_key(self, new_value):
        self.config['secrets']['stream_key'] = new_value
        self.update_config()


    # Stream
    ## Streaming service
    @property
    def streaming_service(self):
        return self.config['stream']['streaming_service']

    @streaming_service.setter
    def tistreaming_servicetle(self, new_value):
        self.config['stream']['streaming_service'] = new_value
        self.update_config()


if __name__ == '__main__':

    config = Config(Path(__file__).parent.parent)
    print(config)

