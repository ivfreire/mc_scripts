import socket, sys
from threading import Thread

class MinecraftClient:
	def __init__(self, nickname='Alice', version='1.16.4'):
		self.nickname	= nickname
		self.version	= version
		self.sock 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected	= False
		self.threads	= []
		print('Instanciated client {}.'.format(nickname))
		return
	
	def connect(self, addr):
		self.addr 		= addr

		print('Connecting to {}:{}...'.format(addr[0], addr[1]))
		self.sock.connect(addr)
		print('Connected!')

		self.join()

		self.threads.append(Thread(target=self.recv, args=[]))
		for thread in self.threads: thread.start()

		self.logic()

		return
	
	def logic(self):
		while self.connected:
			if not self.connected: break
		return

	def join(self):
		payload = b'\x10\x00\xf2\x05\tlocalhostc\xdd\x02\x0f\x00\rKayabaAkihita'
		self.sock.send(payload)
		print('Payload sent!')
		self.connected = True
		return

	def recv(self, bufsize=1024):
		while self.connected:
			data = self.sock.recv(bufsize)
			if len(data) > 0:
				self.read(data)
		return
	
	def send(self, data):
		if self.connected:
			data = str(data, encoding='UTF-8')
			self.sock.send(data)
		return

	def read(self, data):
		if data[0] > 0:
			if data[1] == 3:
				print(data)
		return

	def close(self):
		self.connected = False
		for thread in self.threads: thread.join()
		self.sock.close()
		return



addr = ('localhost', 25565)

mc_client = MinecraftClient(nickname='KayabaAkihito')
mc_client.connect(addr)


mc_client.close()

















'''

\x10		16	# Length
\x00		0	# Length

\xf2		242	# Version
\x05		5	# Version

\t			116	# ?

localhostc		# HOST?
\xdd\x02


\x0f		15	# Length
\x00		0	# Length

\r			114	# ?
KayabaAkihita	# Nickname

'''