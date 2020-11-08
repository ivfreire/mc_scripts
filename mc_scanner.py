import socket, sys, json
from threading import Thread

def main(host, port=25565):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(1)

	sock.connect((host, port))

	data = b'\x10\x00\xf2\x05\tlocalhostc\xdd\x01\x01\x00'
	sock.send(data)

	info = ''.encode('UTF-8')

	recv = True
	while recv:
		try:
			data = sock.recv(1024)
			if len(data) > 0:
				info += data
		except Exception as e:
			recv = False

	sock.close()

	mc_data = json.loads( info[5:].decode('UTF-8') )

	print('{:<48}ONLINE: {}/{}\n'.format(
		mc_data['version']['name'],
		mc_data['players']['online'],
		mc_data['players']['max']
	))

	# print(mc_data)

	return

if __name__ == '__main__':
	main(sys.argv[1])