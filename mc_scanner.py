'''
	This script scan a given ip address for server information, like name
	online players, version, description, favicon etc.
	
	OBS: I am afraid this script will only work out with cracked servers, since
	communication between original servers and clients is encrypted.
'''

import socket, sys, json
from threading import Thread

FLAGS = {
	'show_errors':		False,
	'timeout_limit':	0.5,
	'not_empty':		False,
	'default_port':		25565
}

def scan(host, port=FLAGS['default_port']):
	'''
		Performs the scan of the specified ip address (host) and port.
		Returns a json object that contains the collected information.
	'''

	mc_data = {
		'addr': {
			'host': host,
			'port': port
		}
	}

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(FLAGS['timeout_limit'])

	try:
		sock.connect((host, port))
	except Exception as e:
		mc_data['error'] = e
		return mc_data

	data = b'\x10\x00\xf2\x05\tlocalhostc\xdd\x01\x01\x00'
	sock.send(data)

	info = ''.encode('UTF-8')

	recv = True
	max_empty = 10
	empty = 0
	while recv:
		try:
			data = sock.recv(1024)
			if len(data) > 0:
				info += data
				empty = 0
			else: empty += 1
			if empty >= max_empty: recv = False
		except Exception as e: recv = False

	sock.close()

	try:
		mc_data['data'] = json.loads(info[5:].decode('UTF-8'))
	except Exception as e:
		mc_data['error'] = e
		return mc_data

	return mc_data

def show(data):
	'''
		Prints the scanned data to the terminal.
	'''
	if data == None: return
	if 'error' in data:
		if FLAGS['show_errors']:
			print('{:<24} {:<48}'.format(
				'({}:{})'.format(data['addr']['host'], data['addr']['port']),
				str(data['error'])[:48],
			))
		return
	if FLAGS['not_empty'] and data['data']['players']['online'] == 0: return
	print('{:<24} {:<48}ONLINE: {}/{}'.format(
		'({}:{})'.format(data['addr']['host'], data['addr']['port']),
		data['data']['version']['name'][:48],
		data['data']['players']['online'],
		data['data']['players']['max']
	))
	return

def treat_host(host):
	if type(host) != str: return None
	n_host = host.split(':')
	if len(n_host) < 2: n_host.append(25565)
	if n_host[1] == '': n_host[1] = 25565
	n_host[1] = int(n_host[1])
	return n_host

def read_file(path):
	'''
		Reads hosts from file at path.
	'''
	hosts = []
	with open(path, 'r') as file:
		for line in file.readlines():
			line = line.split('\n')[0]
			hosts.append(treat_host(line))
	return hosts

def scan_hosts(hosts):
	for host in hosts:
		data = scan(host[0], host[1])
		show(data)

def main():
	'''
		Controls the execution of the script.
	'''

	for i in range(len(sys.argv)):
		if sys.argv[i] == '-p':
			FLAGS['default_port'] = sys.argv[i+1]
		if sys.argv[i] == '--not-empty':
			FLAGS['not_empty'] = True
		if sys.argv[i] == '--show-errors':
			FLAGS['show_errors'] = True
		if sys.argv[i] == '--timeout-limit':
			FLAGS['timeout_limit'] = float(sys.argv[i+1])
	
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-f':
			hosts = read_file(sys.argv[i+1])
			scan_hosts(hosts)

	return

if __name__ == '__main__':
	main()