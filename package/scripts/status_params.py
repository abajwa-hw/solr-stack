#!/usr/bin/env python
from resource_management import *

# config object that holds the status related configurations declared in the -env.xml file
config = Script.get_config()

solr_piddir = config['configurations']['solr-env']['solr_pid_dir']
solr_port = config['configurations']['solr-env']['solr.port']
solr_pidfile = format("{solr_piddir}/solr-{solr_port}.pid")