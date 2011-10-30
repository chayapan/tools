## cluster.py
#
# Example of a Virtual Box cluster generator
#
# Modify   build(), register(), unregister() to fit your need.
#
import os, sys, os.path
import vbox

class Net:
    def __init__(self, host):
        self.host = host
class Disk:
    format = '.vdi'
    size = '12'
    def __init__(self, id=None, path=''):
        self.id = id
        self.path = path
        self.filename = os.path.join(path,id+self.format)
class Host:
    cpus = '1'
    memory = '128'
    def __init__(self, id=None):
        self.id = id
        self.disk = []
        self.nic = []
        self.sata_ctl = 'sata'     #name SATA controller
    def set_spec(self):
         cmd = ["modifyvm", '"%s"' % self.id]
         cmd.extend(["--cpus",self.cpus])
         cmd.extend(["--memory",self.memory])
         cmd.extend(["--nic1","bridged"])              # http://www.virtualbox.org/manual/ch08.html#idp12476640
         cmd.extend(["--nic2","intnet"])               # Network settings
         #cmd.extend(["--nic2","nat"])
         vbox.vboxmanage(cmd)
         cmd = ["modifyvm", '"%s"' % self.id]
         cmd.extend(["--intnet1","intnet1"])
         cmd.extend(["--bridgeadapter1",'"%s"' % "Broadcom 802.11n Network Adapter"]) # list bridgedifs
         #  cmd.extend(["--hostonlyadapter1",'"%s"' % "VirtualBox Host-Only Ethernet Adapter"])  # list hostonlyifs
         vbox.vboxmanage(cmd)
    def attach_hdd(self):
        vbox.add_sata_ctl(self.id,self.sata_ctl)
        port = 0
        for disk in self.disk:
            vbox.attach_hdd(self.id,self.sata_ctl, disk.filename, port)
            port = port+1
        return self
class Cluster:
    prototype_disk=None
    disk = []
    host = []
    def __init__(self):
        self.HOME = os.path.abspath(os.getcwd())
        # os.chdir(self.HOME)
    def newHost(self, id):
        vbox.create_vm(id, self.HOME)
        host = Host(id)
        self.host.append(host)
        return host
    def build(self):
        # clone disk from prototype
        # SRC_HDD = '''C:\Users\chayapan\VirtualBox VMs\\erp01.vdi'''
        # vbox.clone_hdd(SRC_HDD,'clone.vdi')
        
        # create new disk
        # vbox.create_hdd(os.path.join(self.HOME,"test"),"12")
        # self.disk.append(Disk('test'))
        
        # create new vm
        # hostname = "VM 1"
        # vbox.create_vm(hostname, self.HOME)
        # self.host.append(Host(hostname))  # Add vm to the cluster
        # self.host[0].disk.append(self.disk[0])  # Add harddisk to the vm
        
        ###
        # Example cluster:
        # 3 hosts , clone.vdi
        for hostname in ['h1', 'h2', 'h3']:
          host = self.newHost(hostname)
          host.disk.append(Disk(hostname+'_1'))
        
        ctl = 'build.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
        ###########################################
        # Also build.... Register , Unregister , Clean , Power On, Power Off, Reset
        self.register(); self.unregister(); self.clean(); self.poweron(); self.poweroff(); self.reset();
    def clean(self):
        self.register()
        for host in self.host:
            vbox.unregister_vm(host.id, True) # Delete everything
        ctl = 'clean.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
    def register(self):
        for host in self.host:
            vbox.register_vm(host.id,self.HOME)
            host.attach_hdd().set_spec()
        ctl = 'cluster_register.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
    def unregister(self):
        for host in self.host:
            vbox.unregister_vm(host.id, False) # Only unregister, not delete
            for disk in host.disk:
              vbox.vboxmanage(["closemedium", "disk", disk.filename])
			ctl = 'cluster_unregister.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
    def poweron(self,headless=False):
        for host in self.host:
            vbox.poweron_vm(host.id)     
        ctl = 'cluster_power_on.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
    def poweroff(self):
        for host in self.host:
            vbox.poweroff_vm(host.id)    
        ctl = 'cluster_power_off.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()
    def reset(self):
        for host in self.host:
            vbox.reset_vm(host.id)       
        ctl = 'cluster_reset.bat'
        f=open(ctl,"w");f.write(vbox.history_flush());f.close()