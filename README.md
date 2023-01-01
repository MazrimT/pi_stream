# pi_stream
Application for streaming directly from camera to Youtube with a Raspberry Pi

Tested on:  
* Raspberry Pi 4b (4gb)  
* Raspian OS 64bit  
* microsoft usb webcam  
  
TODO:  
* get a Raspberry Pi HD camera and test/use that instead of usb camera
* get a pi-touch screen and make a gui controlls the stream  
** start/stops the stream  
** connect to a wifi  
** modify secrets.json config
** modify stream_config.toml

# Install
(assumes a clean install of Raspian OS with internet connection)

Install some things  
```bash 
sudo apt-get install git            # to clone this repo
sudo apt-get install python3        # to run python code
sudo apt-get install ffmpeg         # video software used
```

Clone the repo
```bash
mkdir ~/git                                         # make a directory for git projects
cd ~/git                                            # cd to the directory
git clone git@github.com:MazrimT/pi_stream.git      # clone this repo
```

Setup things for Python
```bash
python -m venv venv                         # create a virtual environment
source /venv/bin/activate                   # switches to the virtual environments python enterpreter
python -m pip install --upgrade pip         # upgrades pip in virtual environment to latest version
python setup.py install                     # installs required python packages
```

# Run
* Put your Stream Key and API key in config/secrets.json  
* set up the stream in config/stream_config.toml

This can't actually run yet, but when it can the idea is to:
this doesn't work yet, but idea is to do:
```bash
# in the virtual environment
python pi_stream/app.py
```

Eventually the idea will be that the app that controlls the touchscreen will start first and be in crontab as run on reboot.