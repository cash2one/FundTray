#!/bin/sh
PROCESS="/home/ubuntu/FundTray/server/workspace/common_server/service_mgr/start.py"
chmod +x $PROCESS
PIDFILE=/tmp/FundTray/service_mgr.pid
start-stop-daemon -K -R 5 -q -p $PIDFILE > /var/log/FundTray.log 2>&1
start-stop-daemon -S -q -b -m -p $PIDFILE -a $PROCESS -- --is_extranet 1 --sm_ip 172.31.25.46 --db_host homeinternet.cbqukcpsqvpy.ap-southeast-1.rds.amazonaws.com --db_port 3306 --db_name service_mgr --db_user homeinternet --db_password HomeInternet