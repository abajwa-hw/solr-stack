#!/bin/bash
set -e 

#Path to install Solr to e.g. /opt/solr
SOLR_PATH=$1

#Url to download Solr from
SOLR_DOWNLOAD_LOCATION=$2

#solr user e.g. solr
SOLR_USER=$3

if [ ! -d "$SOLR_PATH" ]
then
    echo "Solr not found..installing"
    
    getent passwd $SOLR_USER
	if [ $? -eq 0 ]; then
    	echo "the user exists, no need to create"
	else
    
	    echo "creating solr user"
	    adduser $SOLR_USER
	fi

    mkdir $SOLR_PATH
    chown solr $SOLR_PATH

	hadoop fs -test -d /user/$SOLR_USER
	if [ $? -eq 0 ]; then
    	echo "Creating user dir in HDFS"
    	sudo -u hdfs hdfs dfs -mkdir -p /user/$SOLR_USER
	fi
	
    #download solr tgz and untar it
    echo "Downloading Solr"
    cd $SOLR_PATH
    wget $SOLR_DOWNLOAD_LOCATION -O solr.tgz
    tar -xvzf solr.tgz
    ln -s solr-* latest
    echo "Solr install complete"	
fi
