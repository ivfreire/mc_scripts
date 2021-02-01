'''
	This script uses a nmap implementation in Python to scan for hosts where there are Minecarft servers running on.
	With this tool, it is even possible to scan for private servers where you can connect for  griefing.
'''

import nmap
import sys

FLAGS = {
	'host': '127.0.0.1',
	'port':	'25565',
	'path':	'result.txt'
}

def scan():
	ps = nmap.PortScanner()
	ps.scan(FLAGS['host'], FLAGS['port'])
	return ps

def save(ps):
	with open(FLAGS['path'], 'w') as log:
		for host in ps.all_hosts():
			data = ps[host]
			if data['tcp'][25565]['state'] == 'open':
				print('{}\t{}\t{}'.format(
					data['addresses']['ipv4'],
					data['hostnames'][0]['name'],
					data['tcp'][25565]['version'],
				))
				log.write('{}\n'.format(
					data['addresses']['ipv4']
				))
	return

def main():
	for i in range(len(sys.argv)):
		if sys.argv[i] == '-w':
			FLAGS['path'] = sys.argv[i+1]

	FLAGS['host'] = sys.argv[1]
	ps = scan()
	save(ps)
	return

if __name__ == '__main__':
	main()
