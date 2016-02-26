#!/usr/bin/env python

"""

(\ _________________
<))_____TORpydo_____)
(/

"""
import socket, requests
from bs4 import BeautifulSoup

__author__ = "TORpydo[at]mailinator.com"

class TOR_ctrl(object):
	"""
	This module provides a simple interface for TOR. It provides a method to change exit node, and a method
	to check that change was effective.
	"""
	def __init__(self, http_proxy='http://127.0.0.1:8118', TOR_ctrl_port=9051):
		"""
		Sets up the class.
		"""
		self.TOR_ctrl_port = TOR_ctrl_port
		self.real_ip = socket.gethostbyname(socket.gethostname())
		self.proxy = {'http' : http_proxy}

	def change_exit_ip(self):
		"""
		Signals TOR control to change exit node. Returns True if all commands go down the socket. Otherwise
		raises exception.
		"""
		_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		_socket.connect(('localhost', self.TOR_ctrl_port))
		commands = ['authenticate ""', 'signal newnym', 'quit']
		try:
			for command in commands:
				_socket.send("%s\r\n"%(command))
			return(True)
		except Exception as e:
			raise(e)

	def chk_exit_ip(self,ip):
		"""
		Checks to see if the ip address is successfully not equal to the ip given.
		Returns new ip if ip has changed. Returns False if it is not.
		Need to find a better site. ipchicken does not like TOR. Turnes out that
		ipchicken uses cloudflare, which when it sees TOR addresses displays the ip
		address back to the user, and throws a cpatcha... thus entirely negating 
		the point of the captcha... SMDH
		"""
		try:
			r = requests.get('http://www.ipchicken.com', proxies=self.proxy)
			if ip not in r.text:
				soup = BeautifulSoup(r.text, 'html.parser')
				bs = soup.find_all('b')
				bs = [str(b.text).strip('\n').split(' ') for b in bs]
				ip = bs[0][0]
				return(ip)
			else:
				return(False)
		except Exception as e:
			raise(e)




def logger(func):
	"""
	Simple logging decorator.
	"""
	def inner(*args, **kwargs): 
		with open('.py_log.txt','a') as lfile:
			ret = func(*args, **kwargs)
			msg = args, kwargs , str(func.__name__), int(time.time()*1000), ret
			lfile.write(str(msg))
			lfile.write('\r\n')
		return (ret)
	return (inner)