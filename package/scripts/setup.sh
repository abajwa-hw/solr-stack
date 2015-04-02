#!/bin/bash
set -e 

#Path to install Solr to e.g. /opt/solr
SOLR_PATH=$1

#Url to download Solr from
SOLR_DOWNLOAD_LOCATION=$2


if [ ! -d "$SOLR_PATH" ]
then
    echo "Solr not found..installing"
    
    echo "adding solr user"
	adduser solr
	mkdir $SOLR_PATH
	chown solr $SOLR_PATH

    echo "Creating HDFS dir"
	sudo -u hdfs hdfs dfs -mkdir -p /user/solr
	sudo -u hdfs hdfs dfs -mkdir -p /user/solr/data
	
	#download solr tgz and untar it
	echo "Downloading Solr"
	cd $SOLR_PATH
	wget $SOLR_DOWNLOAD_LOCATION -O solr.tgz
	tar -xvzf solr.tgz
	ln -s solr-* latest
	echo "Solr install complete"	
fi
