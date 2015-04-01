#!/usr/bin/env python
from resource_management import *

config = Script.get_config()

stack_piddir = config['configurations']['solr-env']['stack_piddir']
stack_pidfile = format("{stack_piddir}/solr.pid")