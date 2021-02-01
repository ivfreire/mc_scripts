import socket

def ping_server(hostname, port=25565):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((hostname, port))

	

	return None

class Bot:
	def __init__(self, nickname='BootyBot_alpha_1.0', host='localhost', port=25565, version=None):
		self.nickname = nickname
		
		ping_server(self.host, self.port)

Bot()