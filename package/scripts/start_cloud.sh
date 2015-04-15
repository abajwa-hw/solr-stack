#!/bin/bash

#Path to start.jar e.g. /opt/solr
SOLR_PATH=$1

#Logfile e.g. /var/log/solr.log
LOGFILE=$2

#pid file e.g. /var/run/solr.pid
PID_FILE=$3

#path containing start.jar file e.g. /opt/solr/latest/server
START_PATH=$4

#zookeeper hosts
ZOOKEEPER_HOSTS=$5

echo "Found zookeepers on: $ZOOKEEPER_HOSTS"  >> $LOGFILE	
 
PID_DIR=$(dirname "$PID_FILE")

#Create pid dir if it does not exist
if [ ! -d "$PID_DIR" ]
then
	echo "Creating PID_DIR: $PID_DIR"  >> $LOGFILE	
	mkdir -p $PID_DIR
fi

#start Solr if not already started from $START_PATH dir
if [ ! -f "$PID_FILE" ]
then
	cd $SOLR_PATH/latest/bin
	echo "Starting Solr Cloud..." >> $LOGFILE	
	OUTPUT=`./solr start -cloud -z $ZOOKEEPER_HOSTS -noprompt`
	echo $OUTPUT >> $LOGFILE	
	PID=`echo $OUTPUT | sed -e 's/.*pid=\(.*\)).*/\1/'`
	echo $PID > $PID_FILE
	echo "Started pid $PID"	 >> $LOGFILE	
else
	echo "PID_FILE $PID_FILE present. Not starting Solr Cloud"	 >> $LOGFILE	
fi


