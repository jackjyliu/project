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

sudo pip3 install flask flask-caching requests celery redis pandas geopandas plotly psycopg2-binary

# install redis server
#sudo wget http://download.redis.io/redis-stable.tar.gz
#sudo tar xvzf redis-stable.tar.gz
#cd redis-stable
#sudo make
#sudo mkdir /etc/redis
#sudo mkdir /var/redis
#sudo cp src/redis-server /usr/local/bin/
#sudo cp src/redis-cli /usr/local/bin/
#sudo cp utils/redis_init_script /etc/init.d/redis_6379
#sudo cp redis.conf /etc/redis/6379.conf
#sudo mkdir /var/redis/6379
