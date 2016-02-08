#### An Ambari Stack for Solr
Ambari stack for easily installing and managing Solr on HDP cluster

- Download HDP 2.2 sandbox VM image (Sandbox_HDP_2.2_VMware.ova) from [Hortonworks website](http://hortonworks.com/products/hortonworks-sandbox/)
- Import Sandbox_HDP_2.2_VMware.ova into VMWare and set the VM memory size to 8GB
- Now start the VM
- After it boots up, find the IP address of the VM and add an entry into your machines hosts file e.g.
```
192.168.191.241 sandbox.hortonworks.com sandbox    
```
- Connect to the VM via SSH (password hadoop) and start Ambari server
```
ssh root@sandbox.hortonworks.com
/root/start_ambari.sh
```
- If you are running on sandbox, Solr is already installed under /opt/solr. You can either rename this dir or install the service to different dir 
```
mv /opt/solr /opt/solr-orig
```
- To deploy the Solr stack, run below
```
VERSION=`hdp-select status hadoop-client | sed 's/hadoop-client - \([0-9]\.[0-9]\).*/\1/'`
sudo git clone https://github.com/abajwa-hw/solr-stack.git /var/lib/ambari-server/resources/stacks/HDP/$VERSION/services/SOLR
```

- Restart Ambari
```
#on sandbox
sudo service ambari restart

#on non-sandbox
sudo service ambari-server restart

```
- Then you can click on 'Add Service' from the 'Actions' dropdown menu in the bottom left of the Ambari dashboard:

On bottom left -> Actions -> Add service -> check Solr service -> Next -> Next -> Next -> Deploy

- Also ensure that the install location you are choosing (/opt/solr by default) does not exist

- On successful deployment you will see the Solr service as part of Ambari stack and will be able to start/stop the service from here:
![Image](../master/screenshots/1.png?raw=true)

- You can see the parameters you configured under 'Configs' tab
![Image](../master/screenshots/2.png?raw=true)



#### Option 2: Automated deployment of fresh cluster via blueprint

- Bring up 4 VMs imaged with RHEL/CentOS 6.x (e.g. node1-4 in this case)

- On non-ambari nodes, install ambari-agents and point them to ambari node (e.g. node1 in this case)
```
export ambari_server=node1
curl -sSL https://raw.githubusercontent.com/seanorama/ambari-bootstrap/master/ambari-bootstrap.sh | sudo -E sh
```

- On Ambari node, install ambari-server
```
export install_ambari_server=true
curl -sSL https://raw.githubusercontent.com/seanorama/ambari-bootstrap/master/ambari-bootstrap.sh | sudo -E sh
yum install -y git
git clone https://github.com/abajwa-hw/solr-stack.git /var/lib/ambari-server/resources/stacks/HDP/2.3/services/SOLR
```


- Ensure Solr is only started after Zookeeper
  - Edit the `/var/lib/ambari-server/resources/stacks/HDP/2.3/role_command_order.json` file to include below:
```
"SOLR_MASTER-START" : ["ZOOKEEPER_SERVER-START"],
```    

- Ensure that by default, Solr is started on multiple nodes (3 in this example)
  - Edit the `/var/lib/ambari-server/resources/stacks/HDP/2.0.6/services/stack_advisor.py` file
from:
```
  def getMastersWithMultipleInstances(self):
    return ['ZOOKEEPER_SERVER', 'HBASE_MASTER']      
```
```
  def getCardinalitiesDict(self):
    return {
      'ZOOKEEPER_SERVER': {"min": 3},
      'HBASE_MASTER': {"min": 1},
      }
```
to:
```
  def getMastersWithMultipleInstances(self):
    return ['ZOOKEEPER_SERVER', 'HBASE_MASTER','SOLR_MASTER']
```
```
  def getCardinalitiesDict(self):
    return {
      'ZOOKEEPER_SERVER': {"min": 3},
      ’SOLR_MASTER': {"min": 3},
      'HBASE_MASTER': {"min": 1},
      }
      
```

- Restart Ambari
```
service ambari-server restart
service ambari-agent restart    
```

- Confirm 4 agents were registered and agent remained up
```
curl -u admin:admin -H  X-Requested-By:ambari http://localhost:8080/api/v1/hosts
service ambari-agent status
```

- (Optional) - Generate Ambari Blueprint and cluster file using Ambari recommendations API using below steps.  
For more details, on the bootstrap scripts see bootstrap script git

```
yum install -y python-argparse
git clone https://github.com/seanorama/ambari-bootstrap.git

#optional - limit the services for faster deployment

#for minimal services
export ambari_services="HDFS MAPREDUCE2 YARN ZOOKEEPER HIVE SOLR"

#for most services
#export ambari_services="ACCUMULO FALCON FLUME HBASE HDFS HIVE KAFKA KNOX MAHOUT OOZIE PIG SLIDER SPARK SQOOP MAPREDUCE2 STORM TEZ YARN ZOOKEEPER SOLR"

export deploy=false
cd ambari-bootstrap/deploy
bash ./deploy-recommended-cluster.bash
```

- Configure your Solr install by editting `/root/ambari-bootstrap/deploy/tempdir*/blueprint.json`. For example to include configurations for Ranger audits in Solr make below changes:
```
    {
      "solr-config": {
        "solr.datadir": "/opt/ranger_audit_server",
        "solr.download.location": "HDPSEARCH",
        "solr.znode":"/ranger_audits"
        }  
    },
    {
      "solr-env": {
        "solr.port": "6083"
        }
    },

```
- Register Bluprint
```
curl -u admin:admin -H  X-Requested-By:ambari http://localhost:8080/api/v1/blueprints/recommended -d @blueprint.json
```
- Deploy Blueprint
```
curl -u admin:admin -H  X-Requested-By:ambari http://localhost:8080/api/v1/clusters/solrCluster -d @cluster.json
```

#### Use Solr 

- Lauch the Solr webapp via navigating to http://sandbox.hortonworks.com:8983/

- Alternatively, you can launch it from Ambari via [iFrame view](https://github.com/abajwa-hw/iframe-view)
![Image](../master/screenshots/3.png?raw=true)



- One benefit to wrapping the component in Ambari service is that you can now monitor/manage this service remotely via REST API
```
export SERVICE=SOLR
export PASSWORD=admin
export AMBARI_HOST=sandbox.hortonworks.com
export CLUSTER=Sandbox

#get service status
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X GET http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#start service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Start $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "STARTED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE

#stop service
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X PUT -d '{"RequestInfo": {"context" :"Stop $SERVICE via REST"}, "Body": {"ServiceInfo": {"state": "INSTALLED"}}}' http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
```
#### Remove Solr service

- To remove the Solr service: 
  - Stop the service via Ambari
  - Delete the service
  
```
export SERVICE=SOLR
export PASSWORD=admin
export AMBARI_HOST=sandbox.hortonworks.com
export CLUSTER=Sandbox    
curl -u admin:$PASSWORD -i -H 'X-Requested-By: ambari' -X DELETE http://$AMBARI_HOST:8080/api/v1/clusters/$CLUSTER/services/$SERVICE
```
  - Remove artifacts 
  
    ```
    rm -rf /var/lib/ambari-server/resources/stacks/HDP/2.2/services/solr-stack
    rm -rf /opt/solr
    ```
  - Restart Ambari
    ```
    service ambari restart
    ```