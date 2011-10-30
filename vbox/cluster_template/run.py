import vbox, cluster
print "Test Clusters"
c = cluster.Cluster()
print c.HOME
print vbox.VBOXMANAGE
c.build()
SRC_HDD = '''C:\Users\chayapan\VirtualBox VMs\\erp01.vdi'''
#target = "F:\controller1.vdi"


"""  list  bridgedifs
     list  hostonlyifs"""