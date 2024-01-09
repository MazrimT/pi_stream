from pathlib import Path
import json
import tomlkit


class Config(object):

    def __init__(self, app_path):
        self.app_path = app_path
        self.config_file = f"{app_path}/config/config.toml"
        self.config = self.read_config()
        
        # set values that should be set at startup
        self.config['streaming'] = "off"
        self.config['stream_process_id'] = 0
        
        # set the config so streaming is off
        self.update_config()

    def __str__(self):
        return json.dumps(self.read_config())

    
    def read_config(self):
        with open(self.config_file, 'rt', encoding='utf-8') as f:
            return tomlkit.load(f)

    def update_config(self):
        # also update the config file
        with open(self.config_file, mode="wt", encoding="utf-8") as fp:
            tomlkit.dump(self.config, fp)

    def set_config(self, key, value):
        pass

    # Stream Key
    @property
    def stream_key(self):
        return self.config['stream_key']

    @stream_key.setter
    def stream_key(self, new_value):
        self.config['stream_key'] = new_value
        self.update_config()


    # Streaming service
    @property
    def streaming_service(self):
        return self.config['streaming_service']

    @streaming_service.setter
    def streaming_service(self, new_value):
        self.config['streaming_service'] = new_value
        self.update_config()

    # Streaming
    @property
    def streaming(self):
        return self.config['streaming']

    @streaming.setter
    def streaming(self, new_value):
        self.config['streaming'] = new_value
        self.update_config()

    # Resolution
    @property
    def resolution(self):
        return self.config['resolution']

    @resolution.setter
    def resolution(self, new_value):
        self.config['resolution'] = new_value
        self.update_config()


    # Streaming process id
    @property
    def stream_process_id(self):
        return self.config['stream_process_id']

    @stream_process_id.setter
    def stream_process_id(self, new_value):
        self.config['stream_process_id'] = new_value
        self.update_config()




if __name__ == '__main__':

    config = Config(Path(__file__).parent.parent)
    print(config)

