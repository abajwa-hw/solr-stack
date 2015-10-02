#!/usr/bin/env python
from resource_management import *
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()


# store the log file for the service from the 'solr.log' property of the 'solr-config.xml' file
stack_log_dir = config['configurations']['solr-config']['solr.log.dir']
stack_log = stack_log_dir+'/solr.log'

solr_cloudmode = config['configurations']['solr-config']['solr.cloudmode']
solr_dir = config['configurations']['solr-config']['solr.dir']
solr_downloadlocation = config['configurations']['solr-config']['solr.download.location']
solr_startpath = config['configurations']['solr-config']['solr.start.path']
solr_user = config['configurations']['solr-config']['solr.user']

#get comma separated list of zookeeper hosts from clusterHostInfo
zookeeper_hosts = ",".join(config['clusterHostInfo']['zookeeper_hosts'])


solr_env_content = config['configurations']['solr-env']['content']

#e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.2/services/solr-stack/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]