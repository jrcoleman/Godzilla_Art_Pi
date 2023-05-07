# EInk Display Deployment - Raspberry Pi

## Enable SPI Interface
```
sudo raspi-config
Choose Interfacing Options -> SPI -> Yes Enable SPI interface
sudo reboot
```

## Install Dependencies
```
sudo apt-get update
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install python3-numpy
sudo pip3 install RPi.GPIO
sudo pip3 install spidev
```

##

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
### Create Worker Deamon
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
# here we have a single node
CELERYD_NODES="local1 api1"
# or we could have three nodes:
#CELERYD_NODES="w1 w2 w3"

# Absolute or relative path to the 'celery' command:
CELERY_BIN="/usr/local/bin/celery"
#CELERY_BIN="/virtualenvs/def/bin/celery"

# App instance to use
# comment out this line if you don't use an app
CELERY_APP="tasks"
# or fully qualified:
#CELERY_APP="proj.tasks:app"

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
#CELERYBEAT_PID_FILE="/var/run/celery/beat.pid"
#CELERYBEAT_LOG_FILE="/var/log/celery/beat.log"

# options for flower
FLOWER_ADDR="dellbuntu.local"
FLOWER_PORT="5555"
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