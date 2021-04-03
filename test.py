import socket

HOST = '149.56.242.149'
PORT = 25565

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print('Connecting...')
sock.connect((HOST, PORT))
print('Connected!')

sock.send(b'\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x01\x01\x00')

while True:
	data = sock.recv(1024)
	if data != b'':
		print(data)

sock.close()