#!/usr/bin/env python
"""
Managment console


(\ _________________
<))_____TORpydo_____)
(/

	
"""

import shelve, time
from multiprocessing import Pool
from lib import mgmt


proj_mgr = mgmt.proj_mgr()
node_mgr = mgmt.node_mgr()
menu2 = mgmt.Menu({'a': 'b', 'c': 'd'})

def main_menu():
	menu = mgmt.Menu({'1': 'create new project', '2': 'create a nodes', '3': 'deploy a nodes','4': 'list nodes'})
	canary = 1
	while canary != 0:
		try:
			choice = menu.get_input()
			canary = 0
		except Exception as e:
			pass
	if choice == '1':
		mk_proj()
	elif choice == '2':
		mk_nodes()
	elif choice == '3':
		deploy_nodes()
	elif choice == '4':
		print(list_vms())
	elif choice == 'exit':
		print('Thank you for trying TORpydo! BAI')
		exit()
	return()

def list_vms():
	do_mgr = mgmt.do_mgr()
	vms = do_mgr.get_vms()
	for vm in vms:
		print(vm.name, vm.ip_address)

def mk_proj():
	proj_name = raw_input('What would you like to call your new project? ')
	proj_mgr = mgmt.proj_mgr(proj_name)
	proj_mgr.build_dir()


def mk_nodes():
	def get_num():
		try:
			return(int(raw_input("How many nodes would you like to make? If you don't choose a number, it will be 1 ")))
		except Exception as e:
			print(e)
			return(1)
	def get_name():
		try:
			return(str(raw_input('What was that project name again? ')))
		except:
			return('base')
	base = get_name()
	do_mgr = mgmt.do_mgr()
	num_nodes = get_num()
	[do_mgr.mk_vm('{}{}'.format(base,i)) for i in range(num_nodes)]
	time.sleep(5)
	local_store = shelve.open('.local_store',writeback=True) 
	local_store['{}_nodes'.format(base)] = [(vm.ip_address, vm.name) for vm in do_mgr.get_vms()]



def deploy_nodes():
	def check_nodes():
		local_store = shelve.open('.local_store','r') 
		bases = local_store.keys()
		nodes = []
		ips = []
		for base in bases:
			nodes.append(local_store[base])
		nodes = nodes[0]
		for ip in nodes:
			ips.append(ip[0])
		print(ips)
		node_mgr = mgmt.node_mgr()
		for ip in ips:
			print('checking status on {}'.format(ip))
			node_mgr.ip = str(ip)
			node_mgr.chk_node()
			print('{} is up.'.format(ip))
		return(ips)
	proj_name = raw_input('Which project would you like to upload? ')
	proj_mgr = mgmt.proj_mgr(proj_name)
	proj_mgr.mk_pkg()
	ips = check_nodes()
	print('All nodes up. Sending deploy packages')
	print('Sleeping for 30 seconds to let everything come all the way up.')
	time.sleep(30)
	for ip in ips:
		print(ip)
		node_mgr.__init__(str(ip))
		node_mgr.upload('./uploads/{}.tar'.format(proj_name))
	print('All packages uploaded. Unpacking.')
	for ip in ips:
		node_mgr.__init__(str(ip))
		node_mgr.run_cmd('tar -xf ~/{}.tar'.format(proj_name))
	print('Packages up. Running deploy scripts.')
	for ip in ips:
		node_mgr.__init__(str(ip))
		node_mgr.run_cmd('cd {}; ~/{}/build.sh'.format(proj_name, proj_name))
	print('done')




if __name__ == '__main__':
	for i in range(6):
		main_menu()
