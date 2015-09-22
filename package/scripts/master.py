import sys, os, pwd, signal, time
from resource_management import *
from subprocess import call

class Master(Script):

  #Call setup.sh to install the service
  def install(self, env):
  
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    self.configure(env)
    
    #import properties defined in -config.xml file from params class
    import params

    #Ensure the shell scripts in the services dir are executable 
    Execute('find '+params.stack_dir+' -iname "*.sh" | xargs chmod +x')

    #form command to invoke setup.sh with its arguments and execute it
    cmd = params.stack_dir + '/package/scripts/setup.sh ' + params.solr_dir + ' ' + params.solr_downloadlocation + ' ' + params.solr_user + ' >> ' + params.stack_log
    Execute('echo "Running ' + cmd + '"')
    Execute(cmd)


  def configure(self, env):
    import params
    env.set_params(params)

  #Call start.sh to start the service
  def start(self, env):

    #import properties defined in -config.xml file from params class
    import params

    #import status properties defined in -env.xml file from status_params class
    import status_params
    
    #form command to invoke start.sh with its arguments and execute it
    if params.solr_cloudmode:
      cmd = params.stack_dir + '/package/scripts/start_cloud.sh ' + params.solr_dir + ' ' + params.stack_log + ' ' + status_params.stack_pidfile + ' ' + params.solr_startpath + ' ' + params.zookeeper_hosts
    else:
      cmd = params.stack_dir + '/package/scripts/start.sh ' + params.solr_dir + ' ' + params.stack_log + ' ' + status_params.stack_pidfile + ' ' + params.solr_startpath

      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd)

  #Called to stop the service using the pidfile
  def stop(self, env):
  
    #import status properties defined in -env.xml file from status_params class  
    import status_params
    
    #this allows us to access the status_params.stack_pidfile property as format('{stack_pidfile}')
    env.set_params(status_params)
    self.configure(env)

    #kill the instances of solr
    Execute (format('./opt/solr/latest/bin/solr stop -all'))  

    #delete the pid file
    Execute (format("rm -f {stack_pidfile}"))
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
  
    #import status properties defined in -env.xml file from status_params class
    import status_params
    env.set_params(status_params)  
    
    #use built-in method to check status using pidfile
    check_process_status(status_params.stack_pidfile)  



if __name__ == "__main__":
  Master().execute()
