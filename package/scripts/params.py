#!/usr/bin/env python
from resource_management import *
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()



solr_cloudmode = config['configurations']['solr-config']['solr.cloudmode']

solr_downloadlocation = config['configurations']['solr-config']['solr.download.location']
solr_dir = config['configurations']['solr-config']['solr.dir']
solr_znode = config['configurations']['solr-config']['solr.znode']

if solr_downloadlocation == 'HDPSEARCH':
  solr_dir='/opt/lucidworks-hdpsearch/solr'
  solr_bindir = solr_dir + '/bin/'
  cloud_scripts=solr_dir+'/server/scripts/cloud-scripts'  
else:
  solr_bindir = solr_dir + '/latest/bin/' 
  cloud_scripts=solr_dir+'/latest/server/scripts/cloud-scripts'

#if os.path.exists(solr_dir + '/latest/bin/'):
#  solr_bindir = solr_dir + '/latest/bin/' 
#  cloud_scripts=solr_dir+'/latest/server/scripts/cloud-scripts'
  
#elif os.path.exists(solr_dir + '/bin/'):
#  solr_bindir = solr_dir + '/bin/'
#  cloud_scripts=solr_dir+'/server/scripts/cloud-scripts'
#else:
#  solr_bindir = 'UNDEFINED'
#  cloud_scripts= 'UNDEFINED'
  

  
#get comma separated list of zookeeper hosts from clusterHostInfo
zookeeper_hosts = ",".join(config['clusterHostInfo']['zookeeper_hosts'])


solr_user = config['configurations']['solr-env']['solr.user']
solr_group = config['configurations']['solr-env']['solr.group']
# store the log file for the service from the 'solr.log' property of the 'solr-env.xml' file
stack_log_dir = config['configurations']['solr-env']['solr.log.dir']
stack_log = stack_log_dir+'/solr.log'

solr_env_content = config['configurations']['solr-env']['content']

#e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.2/services/solr-stack/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

