import string
from time import sleep
from faker import Faker
from random import randint, choice, randrange
from datetime import datetime, timedelta

def generate_code_20():
	num_1 = ''.join([str(randint(0,9)) for x in range(10)])
	alpha_1 = ''.join([choice(string.letters).lower() for x in range(5)])
	num_2 = str(randint(0,9))
	return num_1 + alpha_1 + num_2
	
def generate_date_currency():
	d = datetime.today()+timedelta(days=randint(0,6))
	d = d.strftime('%y%m%d')
	cur = choice(['EUR','USD'])
	amount = str(randrange(1,1000,1)) + ',' + str(randrange(10,99,1))
	return d + cur + amount
	
def generate_account():
	bankcode = choice(['429811706','238918'])
	account = str(randrange(100000,800000))
	return bankcode + account

def generate_from(fake):
	address = fake.address().split('\n')
	address.insert(1, 'USA')
	address = '\n'.join(address)
	name = fake.name()
	return name +'\n'+ address
	
def create_mt103():	
	fake = Faker('en_US')
	code20 = generate_code_20()
	print('[+] Processing %s' % code20)
	ofile = open('processing/'+code20,'w')
	ofile.write(':20:'+code20+'\n')
	ofile.write(choice([':23B:SPRI',':23B:SSTD'])+'\n')
	ofile.write(':32A:'+generate_date_currency()+'\n')
	ofile.write(':50K:/'+generate_account()+'\n'+generate_from(fake)+'\n')
	ofile.write(':59A:/'+generate_account()+'\n')
	ofile.write(generate_from(fake)+'\n')
	ofile.close()
	
if __name__ == '__main__':
	while 1:
		sleep(randint(1,5))
		create_mt103()