import socket
import sys
from threading import Thread

flags = {
	'nickname':			'wrapper',
	'version':			'1.16.4',
	'dynamic_version':	False
}

def parse_addr(addr):
	if addr != '':
		n_addr = addr.split(':') + [25565]
		n_addr[1] = int(n_addr[1])
		return (n_addr[0], n_addr[1])
	return

class Server():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False
		self.c_socket = None
		print('Created new server socket')
		return
	
	def connect(self, addr):
		self.addr = addr
		try:
			print('Connecting to {}:{}...'.format(addr[0], addr[1]))
			self.sock.connect(addr)
			self.connected = True
			print('Connected!')
		except Exception as e:
			print('Exception at Server: {}'.format(e))
			self.stop()
			return
		return
	
	def recv(self, bufsize=4096):
		try:
			print('Ready for dealing packets.')
			while self.connected:
				data = self.sock.recv(bufsize)
				if len(data) > 0:
					if self.c_socket != None:
						self.c_socket.send(data)
		except Exception as e:
			print('Exception at Server: {}'.format(e))
			self.stop()
		return
	
	def stop(self):
		self.connected = False
		self.sock.close()
		return

class Client():
	def __init__(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connected = False
		self.s_socket = None
		self.timeout_limit = 10
		print('Created new client socket.')
		return
	
	def bind(self, addr):
		self.sock.bind(addr)
		print('Client socket has been binded to {}:{}'.format(addr[0], addr[1]))
		return
	
	def listen(self):
		self.sock.listen(1)
		return
	
	def accept(self):
		print('Awaiting for client connection...')
		self.client = self.sock.accept()
		self.connected = True
		print('Client connected!')
		return
	
	def recv(self, bufsize=4096):
		print('Ready to receive packets!')
		count = 0
		while self.connected:
			data = self.client[0].recv(bufsize)
			if len(data) != 0:
				count = 0
				if self.s_socket != None:
					self.s_socket.send(data)
			else:
				count += 1
				if count == 10: self.stop()
		return
	
	def send(self):
		return
	
	def stop(self):
		self.sock.close()
		self.connected = False
		return

class MinecraftWrapper:
	def __init__(self, addr):
		self.addr = parse_addr(addr)
		self.server_connected = False
		self.is_running = False
		self.client = None
		self.server = None
		self.threads = []
		return
	
	def start(self):
		self.is_running = True
		
		self.threads.append(Thread(target=self.commands, args=[]))
		self.threads[-1].start()

		while self.is_running:
			try:
				self.client = Client()
				self.client.bind(self.addr)
				self.client.listen()
				self.client.accept()

				if self.server == None:
					raise BaseException('Please, first connect the MCWrapper to a server!').with_traceback(tb)

				self.server.c_socket = self.client.client[0]
				self.client.s_socket = self.server.sock

				self.client.recv()
			except Exception as e:
				print('Exception at Client: {}'.format(e))
				self.client.stop()

		return
	
	def commands(self):
		while self.is_running:
			cmd = input('')
			self.parse_cmd(cmd)
	
	def parse_cmd(self, cmd):
		cmd = cmd.split(' ')
		if cmd[0] == 'quit':
			self.stop()
		if cmd[0] == 'connect':
			self.connect_server(parse_addr(cmd[1]))
		return
	
	def connect_server(self, addr):
		self.server = Server()
		self.server.connect(addr)
		self.threads.append(Thread(target=self.server.recv, args=[]))
		self.threads[-1].start()
		return

	def stop(self):
		self.client.stop()
		self.is_running = False

def main():
	mw = MinecraftWrapper(('localhost:25565'))
	mw.start()
	return

if __name__ == '__main__':
	main()