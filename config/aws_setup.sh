#!/bin/bash
sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install python3-pip -y
sudo apt-get install python3-venv -y
sudo apt install git -y
sudo apt-get install supervisor -y
sudo apt-get install nginx -y
sudo apt-get install gunicorn -y

sudo mkdir /home/project
sudo python3 -m venv production-env
source /home/production-env/bin/activate

# install redis server
#wget http://download.redis.io/redis-stable.tar.gz
#tar xvzf redis-stable.tar.gz
#cd redis-stable
#make