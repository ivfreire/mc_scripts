import socket, sys, zlib
from threading import Thread

class MinecraftClient:

	def __init__(self, nickname, version):
		self.nickname = nickname
		self.version = version
		self.state = 0
		return
	
	def connect(self, hostname, port):
		print('Trying to connect to {}:{}...'.format(hostname, port))
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		
		try:
			self.sock.connect((hostname, port))
			print('Connected!')
		except Exception as e:
			print('Exception at connecting: {}'.format(e))
			return

		self.hostname = hostname
		self.login()

		return

	def login(self):
		payload = bytearray(b'\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x02')
		payload += b'\x00'

		print(payload)

		self.sock.send(b'\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x02\x0f\x00\rKayabaAkihita')

		data = self.sock.recv(1024)
		print(data)

		while True:
			print('CU')

		return

mc_client = MinecraftClient('AncapDestroyer', '1.16.4')
mc_client.connect('localhost', 25565)

'''
	242	5

	LENGTH	P_ID	CONTENT
	\x10	\x00	\xf2\x05 \tlocalhost \x0b\xb8 \x02
	\x0f	\x00	\rKayabaAkihito

'''