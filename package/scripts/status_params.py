#!/usr/bin/env python
from resource_management import *

# config object that holds the status related configurations declared in the -env.xml file
config = Script.get_config()

# store the location of the stack service piddir from the 'stack_piddir' property of the 'solr-env.xml' file
stack_piddir = config['configurations']['solr-env']['stack_piddir']
stack_pidfile = format("{stack_piddir}/solr.pid")