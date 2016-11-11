#!/usr/bin/env python
'''
This code is from the Coffee Machine project. It can scan etherscan for a transaction and send commands
to the Raspberry Pi. Modify accordingly for the Beer Machine project. This should help get things started. 

Original author: Richard Moore (ricmoo). 

'''
#from display import lcd
import json
import time
import urllib2

import wiringpi

import RPi.GPIO as GPIO
import time

def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(16, GPIO.OUT)

def turn_on():
	GPIO.output(16, 1)
	print("output1")
	time.sleep(14)
      	GPIO.output(16, 0)

API_KEY = '9D13ZE7XSBTJ94N9BNJ2MA33VMAY2YPIRB';

def get_balance(address, testnet = True):
    to_block = 'latest'

    host = "testnet.etherscan.io"
    if not testnet: host = "etherscan.io"
    url = (("http://%s/api?module=account&action=balance" % host) +
           ("&address=%s" % address.lower()) +
           ("&tag=%s" % to_block) + 
           ("&apikey=%s" % API_KEY))

    #print url

    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/601.7.7 (KHTML, like Gecko) Version/9.1.2 Safari/601.7.7'
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', ua)]
    try:
        req = opener.open(url)
        data = json.loads(req.read())
        #print data
        return int(data['result'])
    except Exception, e:
        raise e

ADDRESS  = '0x02172f0F61361b6a8Ddd3baf729f870BEB628E51'
TESTNET  = True
PRICE    = 10000000000000000 

if __name__ == '__main__':
    setup();
    
    last_balance = get_balance(ADDRESS, TESTNET)
    while True:
        balance = get_balance(ADDRESS, TESTNET)
        print 'Current balance:', balance
        delta_balance = balance - last_balance
        print "Delta balance:", delta_balance
        if delta_balance >= PRICE:
            delta_balance = 0
	    print("Pouring Coffee")
            turn_on()
	    print("Turning off")
	    GPIO.output(16, 0)
	    time.sleep(2)
        last_balance = balance
	time.sleep(2) # set json api query time

#turn_on()
