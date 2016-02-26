

""" This library provides interfaces for DigitalOcean, ssh/scp, menu creation and handling, and project managment

(\ _________________
<))_____TORpydo_____)
(/

BOM:

Wrapper for hosting service APIs to allow for consistent interface at higher levels.
Implemented so far:
	DigitalOcean

Wrapper for sshing to nodes to: (Currently uses os.system() should really fix.)
upload file
download file
run arbitrary command

Project managment class to handle creation of new directories, and taring them to the 
uploads directory.

Menu class to make it easy to handle menus well.

"""

__author__ = 'TORpydo[at]mailinator.com'

import json, random, subprocess
import digitalocean


class Menu(object):
    """
    Class to provide easy menu creation
    Takes a dictionary as Initializetion vector.
    returns True unless argument is not dict in which case raises ValueError
    Adds an exit option to any menu dict passed unless it already exists.
    """
    def __init__(self,options_dict={'a':'a','b':'b','exit':'exit'}):
        """ 
        Initialize with a dictionary of expected user input. Defaults to {'a':'a','b':'b','exit':'exit'}
        If exit is not a key, add an exit key to options_dict 
        """
        if isinstance(options_dict, dict):
            if 'exit' not in options_dict.keys():
                options_dict['exit'] = 'exit'
            self.options_dict = options_dict
        else:
            raise(ValueError)
        return

    def dspl_menu(self):
        """
        Display the options for the user
        """
        print("\nUser input required. Please choose one of the below options.")
        keys = self.options_dict.keys()
        keys.sort()
        for key in keys:
            print("Please enter {} to {}".format(key,self.options_dict[key]))
        return

    def get_input(self):
        """ Return user input, or False. Have not implemented KeyboardInterrupt yet. """
        try:
            self.dspl_menu()
            user_input = raw_input('What choice would you like to make? ')
        except Exception as e:
            raise e
        if user_input not in self.options_dict.keys():
            print('Invalid option selected: {}'.format(user_input))
            raise ValueError
        else:
            return(user_input)
        return


class do_mgr(object):
	""" 
	DigitalOcean wrapper.  
	"""
	def __init__(self,config_file='./etc/sample_DO.cfg'):
		with open(config_file, 'r') as f:
			self.config = json.load(f)
			self.key = self.key_handler()

	def get_vms(self,):
		""" 
		returns a generator of vm objects from DigitalOcean
		"""
		return(digitalocean.Manager(token=str(self.config['token'])).get_all_droplets())
	
	def mk_vm(self,name):
		""" 
		Initiats a build of a server in DO, requires a key may be used as 
		do_mgr.mk_vm('servername',do_mgr.key_handler())
		"""
		return(digitalocean.Droplet(token=self.config['token'],name=name,
			region=random.choice(self.config['regions']), image='ubuntu-14-04-x64',
			size_slug='512mb',backups=False,ssh_keys=[self.key.id]).create())

	def kill_vm(self,name):
		""" 
		A really poor way of killing a VM need to get better at this.
		"""
		vms = self.get_vms()
		for vm in vms:
			if name == vm.name:
				try:
					return(vm.destroy())
				except:
					return(False)
			return(False)

	def key_handler(self,):
		""" 
		Returns a key object for DigitalOcean
		"""
		key = digitalocean.SSHKey(token=self.config['token'])
		return(key.load_by_pub_key(self.config['ssh_key']))


class proj_mgr(object):
	"""
	class for setting up new projects, and tests.
	now uses subprocess.call() woot... one class down!!!!
	"""
	def __init__(self, proj_name='sample_project', skel='./etc/skel/'):
		"""
		It's a damn init method... read it.
		"""
		self.proj_name = proj_name
		self.skel = skel
		return

	def mk_dir(self):
		"""
		Makes a dir in the current dir named self.proj_name. Uses os.system() which is the reason 
		puppies die.
		"""
		return(subprocess.call('mkdir {}'.format(self.proj_name), shell=True))
	
	def build_dir(self):
		"""
		Copies contents of self.skel dir to self.proj_name. Uses os.system() to expedite trip to hell
		"""
		self.mk_dir()
		return(subprocess.call('cp -r {}* ./{}'.format(self.skel, self.proj_name), shell=True))

	def mk_pkg(self):
		"""
		makes a tarball of self.proj_name, and places it in ./uploads
		"""
		return(subprocess.call('tar -cf ./uploads/{}.tar ./{}'.format(self.proj_name, self.proj_name), shell=True))


class node_mgr(object):
	"""
	Class to handle communication with the nodes.
	"""
	def __init__(self,ip='192.168.0.1',user='root'):
		""" 
		Set up connection_string defaults to root user. 
		"""
		self.connection_string = '{}@{}'.format(user,ip)
		self.ip = ip
		self.user = user

	def run_cmd(self,cmd):
		""" 
		Run an arbitrary command string. Returns True if command exits successfully.
		"""
		try:
			subprocess.call('ssh -oStrictHostKeyChecking=no {} "{}"'.format(self.connection_string,cmd), shell=True)
			return(True)
		except Exception as e:
			raise(e)

	def upload(self,file_location,dst_location='~/'):
		""" 
		Upload a file. dst_location defaults to ~/ 
		"""
		try:
			subprocess.call('scp -oStrictHostKeyChecking=no {} {}:{}'.format(file_location, 
				self.connection_string, dst_location), shell=True)
			return(True)
		except Exception as e:
			raise(e)

	def download(self,file_location,dst_location='./downloads/'):
		""" 
		Downlod a file. dst_location defaults to ./downloads/ 
		"""
		try:
			subprocess.call('scp -oStrictHostKeyChecking=no {}:{} {}'.format(self.connection_string, 
				file_location, dst_location), shell=True)
			return(True)
		except Exception as e:
			raise(e)

	def chk_node(self,max_count=100):
		""" 
		Ping node up to max_count times. max_count defaults to 100. If ping responds return True. All other 
		cases return false 
		"""
		for i in range(max_count):
			try:
				if subprocess.call('ping -c 1 {}'.format(self.ip), shell=True) == 0:
					return(True)		
			except Exception as e:
				raise(e)
		return(False)
