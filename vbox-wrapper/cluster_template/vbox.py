''' VirtualBox management '''
import sys,os,subprocess,os.path

VBOX_HOME = '''C:\Program Files\Oracle\VirtualBox'''
VBOXMANAGE = os.path.join(VBOX_HOME,'VBoxManage.exe')
VBOXHEADLESS = os.path.join(VBOX_HOME,'VBoxHeadless.exe')
#print("VirtualBox  wrapper")
#print(VBOXMANAGE)

DRY_RUN = True
HISTORY = []   # command history

def file_exists(path):
    return os.path.exists(path)

def vboxmanage(params):
        line = '"%s"' % VBOXMANAGE + " " + " ".join(params)
        cmd = ['"%s"' % (VBOXMANAGE)]
        cmd.extend(params)
        if (DRY_RUN):
            HISTORY.append(line)
            return line
        try:
          o = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
          print o
        except Exception as e:
          print "exec error"
          print e
    
def clone_hdd(src,dest):
    """Cloning HDD: """
    cmd = vboxmanage(["clonehd", '"%s"' % src, '"%s"' % dest])
def add_sata_ctl(vm,sata="SATA1"):
        """Add SATA Controller"""
        vboxmanage(["storagectl", '"%s"' % (vm), "--name", '"%s"' % (sata), "--add", "sata"])
        return vm
def remove_sata_ctl(vm,sata="SATA1"):
        """Add SATA Controller"""
        vboxmanage(["storagectl", '"%s"' % (vm), "--name", '"%s"' % (sata), "--remove"])
        return vm
def list_hdd():
        vboxmanage(["list", "hdds"])
def list_vm():
        vboxmanage(["list", "vms"])
def showinfo(vm):
        vboxmanage(["showvminfo", vm])
def attach_hdd(vm,ctl,hdd,port=0):
        vboxmanage(["storageattach", '"%s"' % (vm),
                    "--storagectl", ctl,
                    "--medium", '"%s"' % (hdd),
                    "--port", str(port),
                    "--type", 'hdd'
                    ])
def create_hdd(hdd, size):
        vboxmanage(["createhd","--filename",hdd,"--size",size])
def create_vm(vm,base_folder=None,register=None, os_type="Ubuntu_64"): 
        cmd = ["createvm","--name",'"%s"' % (vm),"--ostype", os_type]
        if base_folder != None:
                assert os.path.isdir(base_folder)
                os.chdir(base_folder)
                cmd.extend(["--basefolder",'"%s"' % (base_folder)])
        if register != None:
                cmd.extend(["--register"])
        vboxmanage(cmd)
        return vm
def unregister_vm(vm,delete=True):
        cmd = ["unregistervm", '"%s"' % (vm)]
        if (delete):
          cmd.append("--delete")
        vboxmanage(cmd)
def register_vm(vm,base_folder=''):
        cmd = ["registervm", '"%s.vbox"' % (os.path.join(base_folder,vm,vm)) ]
        vboxmanage(cmd)
def reset_vm(vm):
    vboxmanage(['controlvm', '"%s"' % vm, 'reset'])
def poweroff_vm(vm):
    vboxmanage(['controlvm', '"%s"' % vm, 'poweroff'])
def poweron_vm(vm):
    vboxmanage(['startvm', '"%s"' % vm])
def history_get():
    return "\n".join(HISTORY)
def history_flush():
    cmd = history_get()
    global HISTORY
    HISTORY = []
    return cmd

"""some sanity checking"""
assert file_exists(VBOXMANAGE)      # the program exists
assert file_exists(VBOXHEADLESS)

''' http://www.virtualbox.org/manual/ch08.html#idp12415632
  Basic host:
    modifyvm
     --cpus 1
     --memory  256
     --nic1 bridged
     --bridgeadapter1
     --nic2 intnet
     --intnet1 "net"
VBoxManage list bridgedifs
'''
"""
BASE_FOLDER = "F:\\cluster"
class Machine(object):
  def __init__(self):
    self.name = ""
    self.hdd = []
    self.primary_hdd = None
    self.cpus = "1"               # CPU count
    self.memory = "256"           # RAM
    self.nic1 = "bridged"
    self.nic2 = "intnet"
    self.intnet1 = "net-name"
  def setup(self):
          '''Create and register machine'''
          create_ubuntu_vm(self.name,BASE_FOLDER, True)
  def update(self):
         cmd = ["modifyvm", self.name]
         cmd.extend(["--cpus",self.cpus])
         cmd.extend(["--memory",self.memory])
         cmd.extend(["--nic1",self.nic1])
         cmd.extend(["--nic2",self.nic2])
         vboxmanage(cmd)
         cmd = ["modifyvm", self.name]
         cmd.extend(["--intnet1",self.intnet1])
         vboxmanage(cmd)
"""