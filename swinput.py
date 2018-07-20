
# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.


from twisted.internet import reactor, protocol
from datetime import datetime

class Echo(protocol.Protocol):
	"""This is just about the simplest possible protocol"""
	
	def dataReceived(self, data):
		"As soon as any data is received, write it back."
		print(data)
		errors = ''
		orig_data = data
		data = data.split('\r\n')
		try:
			if ':20:' not in data[0]:
				errors = 'ERR: No Sender Reference\r\n'
			if ':23B:' not in data[1] and len(data[1]) != 8:
				errors = 'ERR: Invalid Operation Code\r\n'
			if ':32A:' not in data[2]:
				errors = 'ERR: No Execution Provided\r\n'
			if 'USD' not in data[2] or 'EUR' not in data[2]:
				errors = 'ERR: No Currency Type Provided\r\n'
			if (datetime.strptime(data[2][5:11],'%y%m%d') - datetime.today()).days < 0:
				errors = 'ERR: Invalid Date'
			if ',' not in data[2] or data[2][14:].replace(',','.') < 0:
				errors = 'ERR: Invalid Currency Amount\r\n'
			if ':50K:' not in data[3]:
				errors = 'ERR: No Ordering Account\r\n'
			if '238918' not in data[3]:
				errors = 'ERR: Invalid Account Number\r\n'
			if ':59A:/' not in data[8]:
				errors = 'ERR: No Beneficiary\r\n'
		except IndexError:
			errors = 'ERR: Not Enough Data'
			
		if errors == '':
			self.transport.send("[+] Processing MT103 (%s)\n [+] %s will be sent from %s to %s" % (data[0].split(":")[-1],data[2][14:].replace(',','.'),data[3].split('/')[-1],data[8].split('/')[-1]))
			ifile = open('processing/'+data[0][5:],'w')
			ifile.write(orig_data)
			ifile.close()
		else:
			ifile = open('failed/'+datetime.today().strftime('%Y%m%d%H%M%S'),'w')
			ifile.write(errors)
			ifile.write(orig_data)
			ifile.close()
		
		
		


def main():
	"""This runs the protocol on port 8000"""
	factory = protocol.ServerFactory()
	factory.protocol = Echo
	reactor.listenTCP(8000,factory)
	reactor.run()

# this only runs if the module was *not* imported
if __name__ == '__main__':
	main()
