import sys, os, pwd, grp, signal, time
from resource_management import *
from subprocess import call

class Master(Script):

  #Call setup.sh to install the service
  def install(self, env):
  
    #import properties defined in -config.xml file from params class
    import params
    import status_params
      
    # Install packages listed in metainfo.xml
    self.install_packages(env)
    
    #e.g. /var/lib/ambari-agent/cache/stacks/HDP/2.3/services/SOLR/package
    service_packagedir = os.path.realpath(__file__).split('/scripts')[0]             
    Execute('find '+service_packagedir+' -iname "*.sh" | xargs chmod +x')

    try: grp.getgrnam(params.solr_group)
    except KeyError: Group(group_name=params.solr_group) 
    
    try: pwd.getpwnam(params.solr_user)
    except KeyError: User(username=params.solr_user, 
                          gid=params.solr_group, 
                          groups=[params.solr_group], 
                          ignore_failures=True)    

    Directory([params.stack_log_dir, status_params.stack_piddir, params.solr_dir],
              mode=0755,
              cd_access='a',
              owner=params.solr_user,
              group=params.solr_group,
              recursive=True
          )


    File(params.stack_log,
            mode=0644,
            owner=params.solr_user,
            group=params.solr_group,
            content=''
    )

    Execute('echo Solr dir: ' + params.solr_dir)
      
    if params.solr_bindir == 'UNDEFINED' or params.cloud_scripts == 'UNDEFINED':
      Execute('echo Error: solr_bin: ' + params.solr_bindir + ' cloud_scripts: ' + params.cloud_scripts)
      Execute('zxzxz')
               
    if params.solr_downloadlocation == 'HDPSEARCH':
      Execute('yum install -y lucidworks-hdpsearch')
        
    #form command to invoke setup.sh with its arguments and execute it
    cmd = params.service_packagedir + '/scripts/setup.sh ' + params.solr_dir + ' ' + params.solr_user + ' >> ' + params.stack_log
    Execute('echo "Running ' + cmd + '" as root')
    Execute(cmd, ignore_failures=True)

    if params.solr_downloadlocation == 'HDPSEARCH':
      Execute('echo HDPSeach mode selected')
    else:
      Execute('cd ' + params.solr_dir + '; wget ' + params.solr_downloadlocation + ' -O solr.tgz -a ' + params.stack_log, user=params.solr_user)
      Execute('cd ' + params.solr_dir + '; tar -xvf solr.tgz', user=params.solr_user)
      Execute('cd ' + params.solr_dir + '; ln -s solr-* latest', user=params.solr_user)
      
    if params.solr_cloudmode:      
      Execute ('echo "Creating znode" ' + params.solr_znode)
      Execute ('echo "' + params.cloud_scripts + '/zkcli.sh -zkhost ' + params.zookeeper_hosts + ' -cmd makepath ' + params.solr_znode + '"')
      Execute (params.cloud_scripts + '/zkcli.sh -zkhost ' + params.zookeeper_hosts + ' -cmd makepath ' + params.solr_znode, user=params.solr_user, ignore_failures=True )  
    
    Execute ('echo "Solr install complete"')



  def configure(self, env):
    import params
    env.set_params(params)
    
    #write content in jinja text field to solr.in.sh
    env_content=InlineTemplate(params.solr_env_content)
    File(format("{params.solr_bindir}/solr.in.sh"), content=env_content, owner=params.solr_user)    
    

  #Call start.sh to start the service
  def start(self, env):

    #import properties defined in -config.xml file from params class
    import params

    #import status properties defined in -env.xml file from status_params class
    import status_params
    self.configure(env)
    
    #form command to invoke start.sh with its arguments and execute it
    if params.solr_cloudmode:
      cmd = params.service_packagedir + '/scripts/start_cloud.sh ' + params.solr_dir + ' ' + params.stack_log + ' ' + status_params.stack_pidfile + ' ' + params.solr_bindir + ' ' + params.zookeeper_hosts + params.solr_znode
    else:
      cmd = params.service_packagedir + '/scripts/start.sh ' + params.solr_dir + ' ' + params.stack_log + ' ' + status_params.stack_pidfile + ' ' + params.solr_bindir

      
    Execute('echo "Running cmd: ' + cmd + '"')    
    Execute(cmd, user=params.solr_user)

  #Called to stop the service using the pidfile
  def stop(self, env):
    import params
     
    #import status properties defined in -env.xml file from status_params class  
    import status_params
    
    #this allows us to access the status_params.stack_pidfile property as format('{stack_pidfile}')
    env.set_params(status_params)
    #self.configure(env)

    #kill the instances of solr
    Execute (format('{params.solr_bindir}/solr stop -all'))  

    #delete the pid file
    Execute (format("rm -f {stack_pidfile}"), user=params.solr_user)
      	
  #Called to get status of the service using the pidfile
  def status(self, env):
  
    #import status properties defined in -env.xml file from status_params class
    import status_params
    env.set_params(status_params)  
    
    #use built-in method to check status using pidfile
    check_process_status(status_params.stack_pidfile)  



if __name__ == "__main__":
  Master().execute()
