import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):
  def install(self, env):
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    import params

    Execute('find '+params.stack_dir+' -iname "*.sh" | xargs chmod +x')
    cmd = params.stack_dir + '/package/scripts/setup.sh ' + params.solr_dir + ' ' + params.solr_downloadlocation + ' >> ' + params.stack_log
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)


  def configure(self, env):
    import params
    #env.set_params(params)

  def start(self, env):
    import params
    import status_params
    cmd = params.stack_dir + '/package/scripts/start.sh ' + params.solr_dir + ' ' + params.stack_log + ' ' + status_params.stack_pidfile + ' ' + params.solr_startpath
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)


  def stop(self, env):
    import status_params
    env.set_params(status_params)
    self.configure(env)
    Execute (format('kill `cat {stack_pidfile}` >/dev/null 2>&1')) 
    Execute (format("rm -f {stack_pidfile}"))
      	

  def status(self, env):
    import status_params
    env.set_params(status_params)  
    check_process_status(status_params.stack_pidfile)  



if __name__ == "__main__":
  Master().execute()
