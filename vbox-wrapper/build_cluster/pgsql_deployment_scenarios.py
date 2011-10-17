# Setup test cluster for PostgreSQL deployment scenarios
#
# There are 4 scenarios, each scenario initially has 2 hosts.

CLUSTER = 'psql_cluster'
def saveCommands():
  f=open(os.path.join(BASE_PATH,'pgcluster_setup_cmds.bat'),'w')
  for l in vbox.HISTORY:
    f.write(l)
    f.write('\n')
  f.close()

scenario = []
class Scenario(object):
  host_count = 2
  def __init__(self, name):
    self.cmd_list = []
    self.name = name
    self.hosts = []
  def name_host(self,hostnum,role='pgdb'):
    return self.name + '_' + role + '%02d' % hostnum
  def new_pgdb(self):
    name = self.name_host( len(self.hosts) + 1 )
    host = Host(name)
    host.num = len(self.hosts) + 1
    self.hosts.append(host)
    return host
class Host(object):
  def __init__(self, name):
    self.scenario = None
    self.num = None
    self.name = name
    self.disk1 = name + '.vdi'

	
# Scenario 1: deployA  --DRBD
#
s1 = Scenario('deployA')
s1_db = [ s1.new_pgdb(),s1.new_pgdb() ]
# Scenario 2: deployB --
#
s2 = Scenario('deployB')
s2_db = [ s2.new_pgdb(),s2.new_pgdb() ]

# Scenario 3: deploy3 --
#
s3 = Scenario('deployC')
s3_db = [ s3.new_pgdb(),s3.new_pgdb() ]

# Scenario 3: deploy3 --
#
s4 = Scenario('deployD')
s4_db = [ s4.new_pgdb(),s4.new_pgdb() ]

scenario = [ s1, s2, s3, s4 ]
################################################################################

hosts = []   #all hosts
[ hosts.extend(s.hosts) for s in scenario ]

hdds = []    #all hdds
[ hdds.append(h.disk1) for h in hosts ]

# Set up system paths
import os, os.path
BASE_PATH = 'F:\\tegan' # base path for the cluster
CLUSTER_FOLDER = os.path.join(BASE_PATH,'cluster')
HDD_FOLDER = os.path.join(BASE_PATH,'hdd')
VM_FOLDER = os.path.join(BASE_PATH,'vm')

import vbox
# Prototypes
PROTOTYPE_HDD = 'C:\Users\chayapan\VirtualBox VMs\erp01.vdi'
INTNET = 'pg-net'

# Setup disks
# If disk doesn't exists, clone from PROTOTYPE
def cloneDisk(target,prototype=PROTOTYPE_HDD):
  if ((not os.path.exists(prototype)) or (not os.path.isfile(prototype))):
    raise Exception('prototype not exists or not a file: PROTOTYPE_HDD')
  if (os.path.exists(target) and os.path.isfile(target)):
    print target + " exists"
  else:
    print target + " not exists, cloning..."
    #do disk cloning
    vbox.clone_hdd(prototype,target)
for disk in hdds:
  cloneDisk(os.path.join(HDD_FOLDER, disk), PROTOTYPE_HDD)

# Create VMs
#
def createVM(name,hdd):
  vbox.create_ubuntu_vm(name,VM_FOLDER, True)
  cmd = ["modifyvm", name]
  cmd.extend(["--cpus","1"])
  cmd.extend(["--memory","256"])
  cmd.extend(["--nic1","bridged"])
  cmd.extend(["--nic2","intnet"])
  cmd.extend(["--intnet1",INTNET])
  vbox.vboxmanage(cmd)

# Cluster set
def cluster_up():
 for h in hosts:
  createVM(h.name,h.disk1)
  vbox.register_vm(os.path.join(VM_FOLDER,h.name,h.name+'.vbox'))
  vbox.add_sata_ctl(h.name,'SATA')
  vbox.attach_hdd(h.name,'SATA',os.path.join(HDD_FOLDER,h.disk1))

# Delete Vms
def cluster_cleanup():
 for h in hosts:
  vbox.unregister_vm(h.name)

cluster_up()
cluster_cleanup()
saveCommands() #save command for actual execution
