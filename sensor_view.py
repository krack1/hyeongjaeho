#!/usr/bin/python
# Author : ipmstyle, https://github.com/ipmstyle
#        : jeonghoonkang, https://github.com/jeonghoonkang

# for the detail of HW connection, see lcd_connect.py
import serial,os,time
import sys
import RPi.GPIO as GPIO
import logging
import logging.handlers

import json
import requests
import fcntl, socket, struct

import sys
sys.path.append("/home/pi/devel/BerePi/apps/lcd_berepi/lib")
from lcd import *
sys.path.append("/home/pi/devel/BerePi/apps/BereCO2/lib")
from co2led import *
DEBUG_PRING = 1
SERIAL_READ_BYTE = 12
FILEMAXBYTE = 1024*1024*100
LOG_PATH = '/home/pi/log_tos.log'

CO2LED_BLUE_PIN = 17
CO2LED_GREEN_PIN = 22
CO2LED_PIN = 27

sensorname = "co2.test"

level = 0
ppm = 0

# set logger file
logger = logging.getLogger(sensorname)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

fileHandler = logging.handlers.RotatingFileHandler(LOG_PATH, maxBytes=FILEMAXBYTE,backupCount=10)
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formatter)
logger.addHandler(fileHandler)

    
def main():
  # Initialise display
  lcd_init()
  print ip_chk(), wip_chk(), mac_chk(), wmac_chk(), stalk_chk()
                    
  while True:

    lcd_string('IP address ', LCD_LINE_1,1)
    lcd_string('MAC eth0, wlan0',LCD_LINE_2,1)
    blue_backlight(False) #turn on, yellow
    time.sleep(2.5) # 3 second delay

    str = ip_chk()
    str = str[:-1]
    lcd_string('%s ET' %str,LCD_LINE_1,1)
    str = mac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    red_backlight(False) #turn on, yellow
    time.sleep(3.5) # 3 second delay

    str = wip_chk()
    str = str[:-1]
    lcd_string('%s WL     ' % (str),LCD_LINE_1,1)
    str = wmac_chk()
    str = str[:-1]
    lcd_string('%s' % (str),LCD_LINE_2,1)
    green_backlight(False) #turn on, yellow
    time.sleep(3.5) # 5 second delay
        
    str = stalk_chk()
    str = str[:-1]
    lcd_string('sTalk Channel' ,LCD_LINE_1,1)
    lcd_string('%s           ' % (str),LCD_LINE_2,1)
    red_backlight(False) #turn on, yellow
    time.sleep(1) # 5 second delay
   
    co = co2_chk()
    lcd_string('CO2 %s' % (co),LCD_LINE_1,1)
    blue_backlight(False)
    time.sleep(3)

    send_data(co)

def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

def ip_chk():
    cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    ipAddr = run_cmd(cmd)
    return ipAddr

def wip_chk():
    cmd = "ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1"
    wipAddr = run_cmd(cmd)
    return wipAddr

def mac_chk():
    cmd = "ifconfig -a | grep ^eth | awk '{print $5}'"
    macAddr = run_cmd(cmd)
    return macAddr

def wmac_chk():
    cmd = "ifconfig -a | grep ^wlan | awk '{print $5}'"
    wmacAddr = run_cmd(cmd)
    return wmacAddr

def stalk_chk():
    cmd = "hostname"
    return run_cmd(cmd)

def co2_chk():
	ppm = 0
    	try:
        	serial_in_device = serial.Serial('/dev/ttyAMA0',38400)
    	except serial.SerialException, e:
        	logger.error("Serial port open error")
        	ledall_off()
	try:
            in_byte = serial_in_device.read(SERIAL_READ_BYTE)
            pos = 0
        except serial.SerialException, e:
            ledall_off()
        if not (len(in_byte) is SERIAL_READ_BYTE) :
            logger.error("Serial packet size is strange, %d, expected size is %d" % (len(in_byte),SERIAL_READ_BYTE))
            print 'serial byte read count error'
            return -1
        # sometimes, 12 byte alighn is in-correct
        # espacially run on /etc/rc.local
        #if not in_byte[9] is 'm':
        #    shift_byte = checkAlignment(in_byte)
        #    in_byte = shift_byte
        if ('ppm' in in_byte):
            if not (in_byte[2] is ' ') :
                ppm += (int(in_byte[2])) * 1000
            if not (in_byte[3] is ' ') :
                ppm += (int(in_byte[3])) * 100
            if not (in_byte[4] is ' ') :
                ppm += (int(in_byte[4])) * 10
            if not (in_byte[5] is ' ') :
                ppm += (int(in_byte[5]))

            logline = sensorname + ' CO2 Level is '+ str(ppm) + ' ppm'
            ledall_off()

	if ppm > 2100 :
                # logger.error("%s", logline)
                # cancel insert data into DB, skip.... since PPM is too high,
                # it's abnormal in indoor buidling
                ledred_on()
                ### maybe change to BLINK RED, later
                return 1
       # else :
       #     logger.info("%s", logline)
 	if ppm < 800 :
            ledblue_on()
        elif ppm < 1000 :
            ledbluegreen_on()
        elif ppm < 1300 :
            ledgreen_on()
        elif ppm < 1600:
            ledwhite_on()
        elif ppm < 1900:
            ledyellow_on()
        elif ppm >= 1900 :
            ledpurple_on()

	return ppm

def send_data(co):
    url = "http://10.255.253.190:4242/api/put"
    data = {
            "metric": "co2.co",
            "timestamp": time.time(),
            "value" : float(co),
            "tags":{
                "host": "hyeongjh"
                }
            }
    ret = requests.post(url, data=json.dumps(data))
    print ret.text

if __name__ == '__main__':

  try:
    main()
  except KeyboardInterrupt:
    pass
  finally:
    lcd_byte(0x01, LCD_CMD)
    lcd_string("Goodbye!",LCD_LINE_1,2)
    GPIO.cleanup()
