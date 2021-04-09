import sys

with open(sys.argv[1], 'r') as source:
	with open(sys.argv[2], 'w') as dest:
		lines = source.readlines()
		for line in lines:
			host = line.split('\t')[0].split(' ')[1]
			if len(host.split('.')) == 4:
				dest.write(host + '\n')