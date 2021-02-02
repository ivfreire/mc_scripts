import socket
from threading import Thread
import struct

class Bot:
	def __init__(self, nickname='BootyBot', version=None, online=False):
		self.nickname = nickname
		self.running = False
		self.state = 0
		self.threads = []
		self.compression = None
		self.logpath = 'bot.log'

		self.log = open(self.logpath, 'w')

	def run(self, hostname='localhost', port=25565):
		self.running = True

		sock = self.connect(hostname, port)

		if sock != None:
			self.threads.append(Thread(target=self.listen, args=[sock, ]))
			self.threads[-1].start()
			self.handshake(sock)
			self.login(sock)
		
		return
	
	def connect(self, hostname, port):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			sock.connect((hostname, port))
			print(f'Connected to {hostname}:{port}')
		except Exception as e:
			print(f'Could not connect to server at {hostname}:{port} for: {e}')
			return None
		return sock

	def listen(self, sock):
		print('Listening to the server.')
		while (self.running):
			packet = sock.recv(4098)
			if packet != '':
				self.handle_packets(packet)
				self.log.write(f'{packet}\n')
		return

	def handle_packets(self, buff):
		length, packet_id, data = buff[0], buff[1], buff[2:]

		if self.state == 2:
			if packet_id == 3: self.set_compression(length - 1, data)	# set compression size
			if packet_id == 0: self.login_success(length - 1, data)		# login response from server

		return

	def set_compression(self, length, data):
		self.compression = struct.unpack('>H', data)
		return
	
	def login_success(self, length, data):
		self.state = 3

		print(data)

		return
	
	def disconnect(self, sock):
		sock.close()
		return

	def handshake(self, sock):
		hostname, port = sock.getpeername()
		print('Performing handshake...')
		sock.send(b'\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x02')
		self.state = 2
		return

	def login(self, sock):
		print('Logging in...')

		data = self.nickname.encode('ASCII')
		data = struct.pack('B', len(self.nickname) + 2) + b'\x00' + struct.pack('B', len(self.nickname)) + data

		sock.send(data)
		return

bot = Bot(nickname='KayabaAkihito')
bot.run()


'''

\x10\x00\xf2\x05\tlocalhost\x0b\xb8\x02
\x0f\x00\rKayabaAkihito




\r\x00\x05\x05en_us\x10\x00\x01\x01\x01\x1a\x00\x0b\x0fminecraft:brand\x07vanilla
\n\x00\x10\x00\x00\x00\x00\x00\xc4\xa6\x0f
\x03\x00\x00\x01
#\x00\x13@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\xc3\x11\xa7\xc9Ak3:\x00
#\x00\x13@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\xc3\x11\xa7\xc9Ak3:\x00
\x03\x00\x15\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01
\x1b\x00\x12@`\xb8/\xd6\x0c_@@P\x80\x00\x00\x00\x00\x00\xc0n\xe5\xaaU\xcdps\x01

'''