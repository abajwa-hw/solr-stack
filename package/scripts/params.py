#!/usr/bin/env python
from resource_management import *
import os

# config object that holds the configurations declared in the -config.xml file
config = Script.get_config()


#e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.3/services/SOLR/package
service_packagedir = os.path.realpath(__file__).split('/scripts')[0]

#shared configs
java64_home = config['hostLevelParams']['java_home']  
#get comma separated list of zookeeper hosts from clusterHostInfo
zookeeper_hosts = ",".join(config['clusterHostInfo']['zookeeper_hosts'])
cluster_name=str(config['clusterName'])

#form the zk quorum string
zookeeper_port=default('/configurations/zoo.cfg/clientPort', None)
#get comma separated list of zookeeper hosts from clusterHostInfo
index = 0 
zookeeper_quorum=""
for host in config['clusterHostInfo']['zookeeper_hosts']:
  zookeeper_quorum += host + ":"+str(zookeeper_port)
  index += 1
  if index < len(config['clusterHostInfo']['zookeeper_hosts']):
    zookeeper_quorum += ","



#####################################
#Solr configs
#####################################


solr_cloudmode = config['configurations']['solr-config']['solr.cloudmode']
solr_downloadlocation = config['configurations']['solr-config']['solr.download.location']
solr_dir = config['configurations']['solr-config']['solr.dir']

solr_znode = config['configurations']['solr-config']['solr.znode']
solr_port = config['configurations']['solr-env']['solr.port']
solr_min_mem = config['configurations']['solr-config']['solr.minmem']
solr_max_mem = config['configurations']['solr-config']['solr.maxmem']
demo_mode = config['configurations']['solr-config']['solr.demo_mode']


if solr_downloadlocation == 'HDPSEARCH':
  solr_dir='/opt/lucidworks-hdpsearch/solr'
  solr_bindir = solr_dir + '/bin'
  cloud_scripts=solr_dir+'/server/scripts/cloud-scripts'  
  server_dir=os.path.join(*[solr_dir,'server'])
else:
  solr_bindir = solr_dir + '/latest/bin' 
  cloud_scripts=solr_dir+'/latest/server/scripts/cloud-scripts'
  server_dir=os.path.join(*[solr_dir,'latest','server'])  

solr_conf = config['configurations']['solr-config']['solr.conf']
if not solr_conf.strip():
  solr_conf=solr_bindir
  
solr_datadir = config['configurations']['solr-config']['solr.datadir']
if not solr_datadir.strip():
  solr_datadir=os.path.join(*[server_dir,'solr'])

solr_data_resources_dir = os.path.join(solr_datadir,'resources')



solr_user = config['configurations']['solr-env']['solr.user']
solr_group = config['configurations']['solr-env']['solr.group']
solr_log_dir = config['configurations']['solr-env']['solr.log.dir']
solr_log = solr_log_dir+'/solr-install.log'

solr_piddir = config['configurations']['solr-env']['solr_pid_dir']
solr_pidfile = format("{solr_piddir}/solr-{solr_port}.pid")

solr_env_content = config['configurations']['solr-env']['content']

solr_xml_content = config['configurations']['solr-xml-env']['content']

solr_log4j_content = config['configurations']['solr-log4j-env']['content']

solr_zoo_content = config['configurations']['solr-zoo-env']['content']
