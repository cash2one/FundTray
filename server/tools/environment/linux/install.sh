#!/bin/sh
export py=python

apt-get install --yes python-dev
apt-get install --yes python-pip
pip install --upgrade --yes setuptools
apt-get install --yes libmysqld-dev
apt-get install --yes uwsgi-plugin-python
apt-get install --yes swig
apt-get install --yes libssl-dev
apt-get install --yes pylint
apt-get install --yes mysql-server mysql-client
apt-get install --yes libfreetype6-dev

cd ../all

pip install setuptools==18.0.1
easy_install pyxmpp2-2.0.0-py2.7.egg


#cd ../../linux
#pip install -r requirements.txt
pip install SQLAlchemy==1.0.2
pip install Cython==0.20.1
pip install MySQL-python==1.2.5
pip install pycrypto==2.6.1
pip install tornado==4.2
pip install DBUtils==1.1
pip install gevent==1.0.2
pip install ujson==1.33
pip install redis==2.10.3
pip install MarkupSafe==0.23
pip install Jinja2==2.7.3
pip install psutil==2.1.3
pip install credis==1.0.3
pip install pymysql==0.6.3
pip install gsocketpool==0.1.3
pip install mprpc==0.1.4
pip install Pillow==2.8.1
pip install gevent-websocket==0.9.5
pip install paho-mqtt==1.1
pip install APScheduler==2.1.1
pip install docutils==0.12

