# pi_stream
WORK IN PROGRESS FOREVER!
I take no responsability for anything working or breaking anything software or hardware.

The idea behind this application is to set up on a raspberry pi with a pi camera attached and have it stream video to youtube or twitch.

 
TODO:  
* make the video have an overlay
* if stream fails for some reason exit the subprocess and set config back to "off"
* move all stream config to config.toml file and a section on the settings page
* make it clearer in settings page that we're streaming maybe button to start/stop?
* get rid of ```Multiple -c, -codec, -acodec, -vcodec, -scodec or -dcodec options specified for stream 0, only the last option '-c:v libx264' will be used.``` message

# prerequisites
* a Raspberry PI with wifi/internet connection.  
* the PI to have a Raspberry PI camera attached.  
* basic knowlage of raspberry pi/linux/git

# Install
(assumes a clean install of Raspian OS with internet connection)

Install Picamera2. 
Very important this step is done first (before the virtual environment)
```bash
sudo apt install -y python3-picamera2 --no-install-recommends
```

Install some things  
```bash 
git clone git@github.com:MazrimT/pi_stream.git      # clone this repo
```

Setup things for Python  
Make sure you are using a virtual environment!  
Certain parts of the code requires this to be set up!
```bash
python -m venv --system-site-packages venv  # create a virtual environment
source venv/bin/activate                    # switches to the virtual environments python enterpreter
python -m pip install --upgrade pip         # upgrades pip in virtual environment to latest version
python -m pip install -r requirements.txt   # installs required python packages
```
VERY IMPORTANT! do not forget the "--system-site-packages" when creating the virtual environment because some things are installed with python3-picamera2 that are not accessible from virutal environment otherwise

Remove the -template from the .flaskenv-template file and fill in your settings.  
The username and password is for the flask admin page and the secret key can be generated however you want, or run the create_secret.py  

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
ruyn run.py                     # for "production"    
```