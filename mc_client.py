import socket, sys, zlib
from threading import Thread

FLAGS ={
	'addr':			('localhost', 25565),
	'nickname':		'viniccius_13',
	'version':		'1.16.4'
}

class MinecraftClient:
	def __init__(self, nickname='mc_client', version='1.16.4'):
		self.nickname	= nickname
		self.version	= version
		self.sock 		= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected	= False
		self.threads	= []
		self.status		= None
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
		self.status = 1

		payload = bytearray(b'\x10\x00\xf2\x03\tlocalhostc\xdd\x02')
		payload += bytes([ len(self.nickname) + 2, 0, len(self.nickname) ])
		payload += self.nickname.encode('UTF-8')

		self.sock.send(payload)
		print('Payload sent!')
		self.connected = True

		return

	def recv(self, bufsize=1024):
		while self.connected:
			data = self.sock.recv(bufsize)
			if len(data) > 0:
				self.parse(data)
		return
	
	def send(self, data):
		if self.connected:
			data = str(data, encoding='UTF-8')
			self.sock.send(data)
		return

	def parse(self, data):
		if len(data) > 0:
			if self.status == 1: self.login_parse(data)
		print(data)
		return
	
	def login_parse(self, data):
		if data[1] == 1:
			self.connected = False
			print('Disconnected!')
		if data[1] == 3:
			print(data)
		return

	def close(self):
		self.connected = False
		for thread in self.threads: thread.join()
		self.sock.close()
		return

def main():
	for i in range(len(sys.argv)):
		if (sys.argv[i] == '-n') or (sys.argv[i] == '--nickname'):
			FLAGS['nickname'] = sys.argv[i+1]
		if (sys.argv[i] == '-v') or (sys.argv[i] == '--version'):
			FLAGS['version'] = sys.argv[i+1]
		if (sys.argv[i] == '-s') or (sys.argv[i] == '--server'):
			FLAGS['addr'] = (sys.argv[i+1], 25565)
	
	client = MinecraftClient(nickname=FLAGS['nickname'], version='1.16.4')
	client.connect(FLAGS['addr'])
	client.close()
	return

if __name__ == '__main__':
	main()