#!/bin/bash
set -e 
#Path to start.jar e.g. /opt/solr
SOLR_PATH=$1

#Logfile e.g. /var/log/solr.log
LOGFILE=$2

#pid file e.g. /var/run/solr.pid
PID_FILE=$3

#path containing start.jar file e.g. /opt/solr/latest/server
START_PATH=$4

PID_DIR=$(dirname "$PID_FILE")

#Create pid dir if it does not exist
if [ ! -d "$PID_DIR" ]
then
	echo "Creating PID_DIR: $PID_DIR"
	mkdir -p $PID_DIR
fi

#start Solr if not already started from $START_PATH dir
if [ ! -f "$PID_FILE" ]
then
	cd $START_PATH
	echo "Starting Solr..."	
	nohup java -jar start.jar >> $LOGFILE 2>&1 &	
	echo $! > $PID_FILE
fi


