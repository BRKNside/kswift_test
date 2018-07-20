from getpass import getpass
from picotui.context import Context
from picotui.dialogs import *
from picotui.screen import Screen
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def runApp():
	getPin()
	mainMenu()
	
def mainMenu():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		rb = WRadioButton(['View Processing Messages','View Failed Messages','Status','Exit'])
		d.add(1, 3, rb)
		b = WButton(8, "OK")
		d.add(10,16,b)
		b.finish_dialog = ACTION_OK
		res = d.loop()
		choice = rb.choice
		if choice not in [0,1,2,3]:
			res = d.loop()
		elif choice == 0:
			procMessage()
		elif choice == 1:
			failMessage()
		elif choice == 2:
			servStatus()
		elif choice == 3:
			os.system('clear')
			os.system('pkill '+str(os.getpid()))

def newMessage():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		res = d.loop()
		
def procMessage():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		msgs = os.listdir('processing')
		msgs.append('Main Menu')
		rb = WRadioButton(msgs)
		d.add(1,3,rb)
		b = WButton(8, "OK")
		d.add(10,16,b)
		b.finish_dialog = ACTION_OK
		res = d.loop()
		choice = rb.choice
		if msgs[choice] == 'Main Menu':
			mainMenu()
		else:
			displayMessage('processing/'+msgs[choice],'proc')
		
def displayMessage(msg,type):
	with Context():
		Screen.cls()
		Screen.attr_reset()
		file_data = open(msg,'r').readlines()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		d.add(1, 2, WLabel(bcolors.OKGREEN+"[+] Viewing " + msg+bcolors.ENDC))
		i = 4
		for item in file_data:
			item.strip('\r\n')
			d.add(1,i,WLabel(item))
			i+=1
		b = WButton(8, "OK")
		d.add(10,20,b)
		b.finish_dialog = ACTION_OK
		res = d.loop()
		if type == 'proc':
			procMessage()
		if type == 'fail':
			failMessage()
		
		
def failMessage():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		msgs = os.listdir('failed')
		msgs.append('Main Menu')
		rb = WRadioButton(msgs)
		d.add(1,3,rb)
		b = WButton(8, "OK")
		d.add(10,16,b)
		b.finish_dialog = ACTION_OK
		res = d.loop()
		choice = rb.choice
		if msgs[choice] == 'Main Menu':
			mainMenu()
		else:
			displayMessage('failed/'+msgs[choice],'fail')
		
def servStatus():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		d = Dialog(5, 1, 50, 12)
		d.add(1, 1, WLabel("SWIFT Debug Interface"))
		d.add(1, 3, WLabel("SWIFT services:"))
		d.add(1, 5, WLabel("Messaging service:  "+bcolors.OKGREEN+"[ OK ]" + bcolors.ENDC))
		d.add(1, 6, WLabel("Processing service: "+bcolors.OKGREEN+"[ OK ]" + bcolors.ENDC))
		d.add(1, 7, WLabel("Debug service:      "+bcolors.WARNING+"[ OK ]" + bcolors.ENDC))
		d.add(1, 8, WLabel("Input service:      "+bcolors.OKGREEN+"[ OK ]" + bcolors.ENDC))
		d.add(1, 11, WLabel("Processing Directory: "+os.popen("du -sh /root/Downloads/swift/processing").read()))	
		d.add(1, 12, WLabel("Failure Directory: "+os.popen("du -sh /root/Downloads/swift/failed").read()))
		b = WButton(8, "OK")
		d.add(10,16,b)
		b.finish_dialog = ACTION_OK
		res = d.loop()
		mainMenu()
		
		
def getPin():
	with Context():
		Screen.cls()
		Screen.attr_reset()
		pin = ''
		while pin != '1234':
			d = DTextEntry(25, '', title='Enter Pin')
			pin = d.result()
		
if __name__ == "__main__":
	runApp()