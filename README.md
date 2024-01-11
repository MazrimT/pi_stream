# pi_stream
WORK IN PROGRESS FOREVER!
I take no responsability for anything working or breaking anything software or hardware.

The idea behind this application is to set up on a raspberry pi with a pi camera attached and have it stream video to youtube or twitch.

 
TODO:  
* get it running on a zero 2 w
* if stream fails for some reason exit the subprocess and set config back to "off". 
    * this happens now if it's closed and when server starts, but not if it fails.
* move all relavent stream config to config.toml file and a section on the settings page.
    * resolution done
* make it clearer in settings page that we're streaming maybe button to start/stop?
* get rid of ```Multiple -c, -codec, -acodec, -vcodec, -scodec or -dcodec options specified for stream 0, only the last option '-c:v libx264' will be used.``` message cause it annoys me.
* set up something that will get a new overlay image from internet source every 10 seconds.
    * save image as app/static/images/overlay.png so stream picks it up automagically.
    * don't lock the setting if streaming so it can be changed on the fly.
* add set_control stuff, like autofocus (not sure if that works to have in the code if not using autofocus enabled camera)

# prerequisites
* a Raspberry PI with wifi/internet connection.  
* the PI to have a Raspberry PI camera attached.  
* basic knowlage of raspberry pi/linux/git

# Install
(assumes a clean install of Raspian OS with internet connection)

## Clone this repo
```bash 
git clone git@github.com:MazrimT/pi_stream.git      # clone this repo
```

## Install Picamera2
```bash
sudo apt install -y python3-picamera2 --no-install-recommends
```
## install ffmpeg
The streaming requires ffmpeg
```bash
sudo apt install ffmpeg
```

## set PULSE_RUNTIME_PATH
set up an environment variable:
`PULSE_RUNTIME_PATH="/run/user/$(id -u)/pulse/"`
Many ways to do this but one example is to put it in users home dir .bash_profile file
This is a requirement for "no audio" to work.

## Setup things for Python  


Connect streaming software to start preview
Viewers will be able to find your stream once you go live
Title
Ras
Make sure you are using a virtual environment!  
Certain parts of the code requires this to be set up!
```bash
python -m venv --system-site-packages venv  # create a virtual environment, --system-site-packages is important! otherwise picamera wont work
source venv/bin/activate                    # switches to the virtual environments python enterpreter
python -m pip install --upgrade pip         # upgrades pip in virtual environment to latest version
python -m pip install -r requirements.txt   # installs required python packages
```
VERY IMPORTANT! do not forget the "--system-site-packages" when creating the virtual environment because some things are installed with python3-picamera2 that are not accessible from virutal environment otherwise

## .flaskenv
Remove the -template from the .flaskenv-template file and fill in your settings.  
The username and password is for the flask admin page and the secret key can be generated however you want, or run the create_secret.py  

## config.toml
Remove the -template from app/config/config.toml-template and if you want add your stream key (can also be added through UI)

if you want set up so the Flask server starts automagically when the PI reboots:
Add the following to crontab so the Flask server starts every on reboot
```bash
@reboot sleep 30 && /[path to git repos]/pi_stream/venv/bin/python3 /[path to git repos]/pi_stream/run.py
```
(the sleep is because I noticed PI's sometimes don't like doing this in the first few seconds after boot and can fail to start things like Flask unless you give it an extra few seconds)


# Run
in virtual environment:
```bash
python run_debug.py             # to test stuff
python run.py                   # for "production"    
```

Browse to http://127.0.0.1:5000/ or IP on what-ever PI it is set up on.  
Username and password were configured in the .flaskenv file
