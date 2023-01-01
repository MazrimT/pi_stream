import json
from pathlib import Path


class Secrets(object):
    
    def __init__(self, config):
        self.config = config
        self.check_secrets()
        
    def __str__(self):
        return json.dumps({
            "stream_key": self.stream_key,
            "api_key": self.api_key
        })
    
    def read_secrets(self):
        """ opens and reads the secrets file 
        """        
        with open(f"{self.config.app_path}/config/secrets.json", "r") as f:
            return json.load(f)
        
    def write_secrets(self, secrets):
        """ overwrites the secrets file
        """
        with open(f"{self.config.app_path}/config/secrets.json", "w") as f:
            f.write(json.dumps(secrets, indent=4))

    @property
    def stream_key(self):
        return self.read_secrets()['stream_key']

    @stream_key.setter
    def stream_key(self, new_key):
        secrets = self.read_secrets()
        secrets['stream_key'] = new_key
        self.write_secrets(secrets)

    @property
    def api_key(self):
        return self.read_secrets()['api_key']

    @api_key.setter
    def api_key(self, new_key):
        secrets = self.read_secrets()
        secrets['api_key'] = new_key
        self.write_secrets(secrets)        

    def check_secrets(self):
        
        secret_keys = ['stream_key', 'api_key']
        # try to read the secrets file and put all keys that should be there in the file
        try:
            secrets = self.read_secrets()
        # if file couldn't be read create an empty file
        except:
            secrets = {}

        for i in secret_keys:
            if i not in secrets.keys():
                secrets[i] = ''
        
        # update secrets
        self.write_secrets(secrets)