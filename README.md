# pi_stream
WORK IN PROGRESS!!!!
I take no responsability for anything working or breaking anything software or hardware.

The idea behind this application is to set up on a raspberry pi with a pi camera attached and have it stream video to youtube or twitch.

 
TODO:  
* make the stream actually work

# prerequisites
Requires:
* a Raspberry PI with wifi/internet connection.  
* the PI to have a Raspberry PI camera attached.  
* basic knowlage of raspberry pi/linux/git

# Install
(assumes a clean install of Raspian OS with internet connection)

Install some things  
```bash 
git clone git@github.com:MazrimT/pi_stream.git      # clone this repo
```

Setup things for Python  
Make sure you are using a virtual environment! Certain parts of the code requires this to be set up!
```bash
python -m venv venv                         # create a virtual environment
source /venv/bin/activate                   # switches to the virtual environments python enterpreter
python -m pip install --upgrade pip         # upgrades pip in virtual environment to latest version
python -m pip install -r requirements.txt   # installs required python packages
```

if you want set up so the Flask server starts automagically when the PI reboots:
Add the following to crontab so the Flask server starts every on reboot
```bash
@reboot sleep 30 && /[path to git repos]/pi_stream/venv/bin/python3 /home/[user]/git/pi_stream/run.py
```
(the sleep is because I noticed PI's sometimes don't like doing this in the first few seconds after boot and can fail to start things like Flask unless you give it an extra few seconds)

# Setup

Remove the -tempalate from the .flaskenv-template file and fill in your settings.  
The username and password is for the flask admin page and the secret key can be generated however you want, or run the create_secret.py  

Add the following to crontab so the Flask server starts every on reboot
```bash
@reboot sleep 30 && /home/[user]/git/pi_stream/venv/bin/python3 /home/[user]/git/pi_stream/run.py
```

# Run
