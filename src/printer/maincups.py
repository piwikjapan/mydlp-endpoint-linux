#!/usr/bin/env python

# Copyright (c) 2012 Ozgen Muzac <ozgen@mydlp.com>
# License GPLv3, see http://www.gnu.org/licenses/gpl.html#content

import sys
import tempfile
import os
from sys import argv
from socket import socket

class DaemonClient():

	def __init__(self, server, port, job_id, user_name, printer_info, file_name):
		self.server = server
		self.port = port
		self.job_id = job_id
		self.printer_info = printer_info
		self.file_name = file_name
		self.user_name = user_name
		self.sock = socket()
		self.sock.connect((self.server, self.port))

	def send(self, message):
		self.sock.sendall(message + "\n")
		response = self.sock.recv(1024).strip()
		return response

	def send_to_daemon(self, file_path):
		message = "file_path: " + file_path
		response = self.send(message)
		if not response.startswith("OK"):
			return True
		
		message = "user_name: " + self.user_name
		response = self.send(message)
		if not response.startswith("OK"):
			return True		

		message = "printer_info: " + self.printer_info
		response = self.send(message)
		if not response.startswith("OK"):
			return True		

		message = "file_name: " + self.file_name
		response = self.send(message)
		if not response.startswith("OK"):
			return True		

		message = "job_id: " + str(self.job_id)
		response = self.send(message)
		if response.startswith("OK"):
			return True
		else:
			return False
	

def start_transfering(job_id, user_name, printer_info, file_name):
	daemon_client = DaemonClient("127.0.0.1", 9100, job_id, user_name, printer_info, file_name)
	fout = tempfile.NamedTemporaryFile(delete=False)
	f = sys.stdin
	text = f.read()
	fout.write(text)
	fout.close()
	response = daemon_client.send_to_daemon(fout.name)
	if response:
		sys.stdout.write(text)

if __name__ == '__main__':
	filelog = open("/home/ozgen/filter.log", "a+b")
	printer_info = os.environ["PRINTER"]
	jobId = int(argv[1])
	user_name = argv[2]
	file_name = argv[3]
	args = argv[0]+" "+argv[1]+" "+argv[2]+" "+argv[3]+" "+argv[4]+" "+argv[5] 
	filelog.write(argv[0]+" "+argv[1]+" "+argv[2]+" "+argv[3]+" "+argv[4]+" "+argv[5])
	start_transfering(jobId, user_name, printer_info, file_name)
