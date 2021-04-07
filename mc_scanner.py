import sys, socket
from json import loads

PORT = 25565

for line in sys.stdin:
	HOST = line.replace('\n', '')

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.settimeout(5)

	try:
	
		sock.connect((HOST, PORT))
		sock.send(b'\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x01\x01\x00')

		data = sock.recv(32767)
		if data != b'':
			data = data[5:].decode('ASCII', errors='ignore')
			data = loads(data)

			desc = data['description']['text']

			print('{:15}\t{:.<63}\t{:<.15}\t{:15}'.format(
				HOST,
				desc,
				'{}:{}'.format(data['version']['name'], data['version']['protocol']),
				'{}/{}'.format(data['players']['online'], data['players']['max'])
			))
		
		sock.close()
	
	except Exception as e:
		print('{}\t{}'.format(HOST, 'Exception: ' + str(e)))