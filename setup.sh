#!/bin/bash

#
# (\ _________________
# <))_____TORpydo_____)
# (/
#


# Check if running as root. Needed for setting up the digital ocean API used.

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Grab and install the python digital ocean API used 
git clone https://github.com/koalalorenzo/python-digitalocean.git ; cd python-digitalocean/ ; python setup.py install ; cd .. ; rm -rf ./python-digitalocean || echo 'Bro... you gonna need to have git.'
