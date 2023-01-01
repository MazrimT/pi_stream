from pathlib import Path
import json
import tomlkit


class Config(object):

    def __init__(self, app_path):
        self.app_path = app_path
        self.config_file = f"{app_path}/config/config.toml"
        self.config = self._read_config()

    #def __str__(self):
    #    return json.dumps({
     #       "app_path": self.app_path.as_posix(),
     #       "config": self.read_config(),
     #   })
    def __str__(self):
        return self.app_path.as_posix()
    
    def _read_config(self):

        with open(self.config_file, 'rt', encoding='utf-8') as f:
            return tomlkit.load(f)

    def update_config(self, section, key, value):
        print(self.config)
        prev_value = self.config[section][key]

        self.config[section][key] = value

        # also update the config file
        with open(self.config_file, mode="wt", encoding="utf-8") as fp:
            tomlkit.dump(config, fp)

        print(section, key, "has been updated from", prev_value, "to", value)

    @property
    def stream_key(self):
        self.config['secrets']['stream_key']


    @stream_key.setter
    def stream_key(self, new_key):
        self.update_config('secrets', 'stream_key', new_key)



if __name__ == '__main__':

    config = Config(Path(__file__).parent.parent)

    #config.stream_key = 'def'

    print(config)