# EInk Display Deployment - Raspberry Pi

## Enable SPI Interface
```
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes Enable SPI interface
sudo reboot
```

## Install PIP and Git
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install git
```
## Get Repo
```
git clone https://github.com/jrcoleman/Godzilla_Art_Pi.git
```
## Install dependencies
```
cd Godzilla_art_pi/display_app
sudo pip install -r requirements.txt
```

## Create Flask Service
- Copy service file to `/etc/systemd/system/flask.service`:  
```
sudo cp system_files/flask.service /etc/systemd/system/flask.service
sudo systemd enable flask
sudo systemd start flask
```  

# AI Server Deployment - Ubuntu 

## Prerequisites
- mdns
```
sudo apt install libnss-mdns
```
- pip
```
sudo apt install python3-pip
```
- Installation Folders
```
sudo mkdir /opt/ai_app
sudo mkdir /opt/ai_app/templates
sudo mkdir /opt/ai_app/static
sudo chown celery:celery /opt/ai_app/static
```
- Other python packages
```
sudo pip install zeroconf
```

## Celery Task Queue
### Install and Configure Redis
Redis is used as the message broker.  
```
sudo apt install redis-server
sudo nano /etc/redis/redis.conf
```
Change `supervised no` to `supervised systemd`.  

### Install Celery Redis
```
sudo pip install -U "celery[redis]"
```
### Create Worker Daemon
- Create celery user:  
```
sudo adduser celery
sudo passwd -d celery
```
- Create celery pid and log directories:  
```
sudo mkdir /run/celery
sudo chown celery:celery /run/celery
sudo mkdir /var/log/celery
sudo chown celery:celery /var/log/celery
```
- Create service file. `/etc/systemd/system/celery.service`:  
```
[Unit]
Description=Celery Service
After=network.target

[Service]
Type=forking
User=celery
Group=celery
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/opt/ai_app
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi start $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
ExecStop=/bin/sh -c '${CELERY_BIN} multi stopwait $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}"'
ExecReload=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP multi restart $CELERYD_NODES \
    --pidfile=${CELERYD_PID_FILE} --logfile=${CELERYD_LOG_FILE} \
    --loglevel="${CELERYD_LOG_LEVEL}" $CELERYD_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target
```  
- Create service config file. `/etc/conf.d/celery`:  
```
# Name of nodes to start
CELERYD_NODES="local1 api1"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"

# App instance to use
CELERY_APP="tasks"

# How to call manage.py
CELERYD_MULTI="multi"

# Extra command-line arguments to the worker
CELERYD_OPTS="--concurrency=1 -Q:local1 local -Q:api1 api"

# - %n will be replaced with the first part of the nodename.
# - %I will be replaced with the current child process index
#   and is important when using the prefork pool to avoid race conditions.
CELERYD_PID_FILE="/run/celery/%n.pid"
CELERYD_LOG_FILE="/var/log/celery/%n%I.log"
CELERYD_LOG_LEVEL="INFO"

# you may wish to add these options for Celery Beat
CELERYBEAT_PID_FILE="/run/celery/beat.pid"
CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"
CELERYBEAT_LOG_LEVEL="INFO"
CELERYBEAT_OPTS="--schedule=/run/celery/celerybeat-schedule"

# options for flower
FLOWER_ADDR="dellbuntu.local"
FLOWER_PORT="5555"
```
### Create Beat Daemon
- Create service file. `/etc/systemd/system/celerybeat.service`:  
```
[Unit]
Description=Celery Beat Service
After=celery.service
PartOf=celery.service

[Service]
Type=simple
User=celery
Group=celery
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/opt/ai_app
ExecStart=/bin/sh -c '${CELERY_BIN} -A ${CELERY_APP} beat \
    --pidfile=${CELERYBEAT_PID_FILE} \
    --logfile=${CELERYBEAT_LOG_FILE} \
    --loglevel="${CELERYBEAT_LOG_LEVEL}" $CELERYBEAT_OPTS'
Restart=always

[Install]
WantedBy=multi-user.target
```
### Install Celery Flower
- Install Application:  
```
sudo pip install flower
```
### Create Flower Daemon
- Create service file. `/etc/systemd/system/flower.service`:  
```
[Unit]
Description=Flower Service
After=celery.service

[Service]
User=celery
Group=celery
EnvironmentFile=/etc/conf.d/celery
WorkingDirectory=/opt/ai_app
ExecStart=/bin/sh -c '${CELERY_BIN} -A $CELERY_APP flower --address=$FLOWER_ADDR --port=$FLOWER_PORT'

[Install]
WantedBy=multi-user.target
```

## Front End Flask App
### Install Flask
```
sudo pip install flask
```
### Create Flask Daemon
- Create service file. `/etc/systemd/system/flask.service`:  
```
[Unit]
Description=Flask Service
After=flower.service

[Service]
User=celery
Group=celery
WorkingDirectory=/opt/ai_app
ExecStart=/bin/sh -c '/usr/local/bin/flask -A front_end run -h dellbuntu.local'

[Install]
WantedBy=multi-user.target
```

## Stable Diffusion Module
### Install Model
- Install Prerequisites:  
```
sudo pip install -U diffusers transformers accelerate scipy safetensors
sudo pip install requests
```
- Clone Model:  
```
sudo apt install git-lfs
git lfs install
git clone https://huggingface.co/stabilityai/stable-diffusion-2-1
sudo mv stable-diffusion-2-1/ /opt/ai_app/
```  

# Known Issues
## ai_app
- Weird lookup issue for .local domains on dellbuntu.
  - Fix: Reserve address and add to hosts file.
- Limit total number of repeat requests on api 503.
- /run/celery not being create on restart.  
## display_app
- Flask service starts on power on, but cannot be connected to until restarted. Probably need to change .service after to something else.
- Flask service should use another user, but I'm too lazy to fix now.
