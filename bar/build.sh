#!/bin/bash

#
# (\ _________________
# <))_____TORpydo_____)
# (/
#

#
# Do not use the packages in Ubuntu's universe. In the past they have not reliably been updated. 
# That means you could be missing stability and security fixes. 
# Well... damn. 
#

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

echo "Build Script running."

echo "deb http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list
echo "deb-src http://deb.torproject.org/torproject.org trusty main" >> /etc/apt/sources.list

gpg --keyserver keys.gnupg.net --recv 886DDD89
gpg --export A3C4F0F979CAA22CDBA8F512EE8CBC9E886DDD89 | apt-key add -

apt-get update
apt-get install tor deb.torproject.org-keyring -qy
apt-get install python-bs4 -qy
apt-get install privoxy -qy

apt-get upgrade -qy

cp ./confs/torrc /etc/tor/torrc
cp ./confs/privoxy_config /etc/privoxy/config

service tor restart
service privoxy restart
