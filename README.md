# Deployment Steps

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