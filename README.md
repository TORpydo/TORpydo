
(\ _________________
<))_____TORpydo_____)
(/

Author: TORpydo[at]mailinator.com


Purpose:
	Provide an extensiable platform to rapidly build and deploy large scale web scanning/scraping projects
	with TOR anonymizing network proxies configured for handeling HTTP/HTTPS/SOCKS.

Requirements:
	git
	https://github.com/koalalorenzo/python-digitalocean.git

Installation: 
	tar -xf ./TORpydo.tar
	cd TORpydo
	sudo ./setup.sh

BOM:
	.
	├── README.md 					# You are here.
	├── bin
	│   └── lib
	│       ├── __init__.py
	│       └── mgmt.py 			# Provides hosting classes and ssh classes
	├── downloads
	├── etc
	│   ├── sample_DO.cfg
	│   └── skel					# Skel dir for nodes.
	│       ├── bin
	│       ├── build.sh
	│       ├── confs				
	│       │   ├── privoxy_config	# Privoxy config file
	│       │   └── torrc			# Tor config
	│       ├── etc
	│       └── lib
	│           ├── __init__.py
	│           └── node_lib.py 	# Provides node interface with TORcontroller and logging decorator.
	├── setup.sh
	├── tests
	│   └── test.py
	└── uploads

11 directories, 11 files

