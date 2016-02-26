#!/usr/bin/env python

"""

(\ _________________
<))_____TORpydo_____)
(/

"""
from lib import mgmt
import time

TORpydo_base = '/Users/ey3/bin/dev/TORpydo'


do_mgr = mgmt.do_mgr('%s/etc/sample_DO.cfg'%(TORpydo_base))
node_mgr = mgmt.node_mgr('1.2.3.4')



# Get key object

try:
	key = do_mgr.key_handler()
	print('Yay!')
except:
	print('do_mgr.key_handler() is broken')

# Make a vm named TESTING

try:
	do_mgr.mk_vm('TESTING',key)
	print('Yay!')
except:
	print('do_mgr.mk_vm() is broken')

print('Sleeping for 30 seconds')
time.sleep(30)

# Print all vms by name and ip if they exist.

try:
	vms = do_mgr.get_vms()
	for vm in vms:
		print(vm.name, vm.ip_address)
	print('Yay!')
except:
	print('do_mgr.get_vms() is broken')
	
# Delete the VM we just made

try:
	do_mgr.kill_vm('TESTING')
	print('Yay!')
except:
	print('do_mgr.kill_vm() is broken')