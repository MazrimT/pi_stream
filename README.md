# pi_stream
WORK IN PROGRESS!!!!
I take no responsability for anything working or breaking anything software or hardware.


Application for streaming directly from camera to Youtube or Twitch with a Raspberry Pi


 
TODO:  
* everything
* fixing login so it's not just open

# Install
(assumes a clean install of Raspian OS with internet connection)

Install some things  
```bash 
sudo apt-get install git            # to clone this repo
sudo apt-get install python3        # to run python code
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
python -m pip install -r requirements.txt   # installs required python packages
```

# Run
  
This assumes you have a raspberry pi that can connect to the internet and that you have a second device on the same network able to connect to it.
  
Put the run.py into cron @reboot to have the flask application that controls the streaming start when the pie boots up.  
```bash
@reboot sleep 30 && /home/[user]/git/pi_stream/venv/bin/python3 /home/[user]/git/pi_stream/run.py
```
This will only start the webserver, not the streaming itself.
