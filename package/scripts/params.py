#!/usr/bin/env python
from resource_management import *

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()

# store the stack service dir from the 'solr.stack.dir' property of the 'solr-config.xml' file
stack_dir = config['configurations']['solr-config']['solr.stack.dir']

# store the log file for the service from the 'solr.log' property of the 'solr-config.xml' file
stack_log = config['configurations']['solr-config']['solr.log']

solr_cloudmode = config['configurations']['solr-config']['solr.cloudmode']
solr_dir = config['configurations']['solr-config']['solr.dir']
solr_downloadlocation = config['configurations']['solr-config']['solr.download.location']
solr_startpath = config['configurations']['solr-config']['solr.start.path']
solr_user = config['configurations']['solr-config']['solr.user']

#get comma separated list of zookeeper hosts from clusterHostInfo
zookeeper_hosts = ",".join(config['clusterHostInfo']['zookeeper_hosts'])