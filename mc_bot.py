import socket
from threading import Thread
import struct
import zlib

def read_varint(data):
	count = 0
	result = 0
	read = 128
	while read & 128 != 0:
		read = data[count]
		value = read & 127
		result |= (value << (7 * count))
		count += 1
	return result, count

def decompress():
	return

class Bot:
	def __init__(self, nickname='BootyBot-alpha-1', version=None, online=False):
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
			packet = sock.recv(2097151)
			if packet != '':
				self.log.write(f'{packet}\n')
				self.handle_packets(packet)
		return

	def handle_packets(self, buff):
		length, index = read_varint(buff[0:])
		
		if self.compression != None:
			data_length, d = read_varint(buff[index:])
			index += d
			if data_length > 0:
				buff = zlib.decompress(buff[index:], bufsize=self.compression)
				length = data_length
				index = 0

		packet_id, d = read_varint(buff[index:])
		index += d
		data = buff[index:]

		if self.state == 2:	# Login state
			if packet_id == 3: self.set_compression(length - 1, data)	# set compression size
			if packet_id == 2: self.login_success(length - 1, data)		# login response from server
		if self.state == 3:
			if packet_id == 36: print(data)
			# print(packet_id)

		# self.log_packet(length, packet_id, data)

		return

	def set_compression(self, length, data):
		self.compression = read_varint(data)[0]
		return
	
	def login_success(self, length, data):
		self.uuid = data[1:17]
		print('Logged in!')
		self.state = 3
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
	
	def log_packet(self, length, packet_id, data):
		self.log.write('{} {} {}\n'.format(length, packet_id, data))
		return


bot = Bot()
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