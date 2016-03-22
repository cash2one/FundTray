#!/bin/sh
PROCESS="/home/ubuntu/FundTray/server/workspace/mmm_da/start.py"
chmod +x $PROCESS
echo "process:"$PROCESS
PIDFILE=/tmp/FundTray/mmm_da.pid
start-stop-daemon -K -R 5 -q -p $PIDFILE > /var/log/mmmda.log 2>&1
start-stop-daemon -S -q -b -m -p $PIDFILE -a $PROCESS -- --is_extranet 1 --sm_ip 172.31.28.109