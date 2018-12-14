import threading, os, time, random
import Adafruit_CharLCD as LCD
import time
import subprocess
import hopper
from scapy.all import *
import os
import json

# Raspberry Pi pin configuration:
lcd_rs        = 25  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 18
lcd_d7        = 22
lcd_backlight = 4

lcd_columns = 16
lcd_rows    = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)

interface = str()

def startPi(config):
    i=0
    started = False
    message = config["welcomeMessage"]
    lcd.message(config["welcomeMessage"])
    time.sleep(5)
    lcd.clear()
    lcd.message('starting')
    while started != True:
        lcd.message('.')
        if i < 4:
            i += 1
        else:
            i = 0
            lcd.clear()
            lcdPrint(message)
        started = isMonitor('wlan%d' % (i-1))
        time.sleep(.5)
    #lcd.clear()
    interface = 'wlan%d' % (i-1)
    startMonitor(interface)
    return interface

def lcdPrint(message):

    lcd.clear()
    lcd.message(message)
    if len(message) > 16:
        for i in range(len(message)):
            time.sleep(0.25)
            lcd.move_left()



def isMonitor(int):
    # we need to determine what Network card is
    # 9c:ef:d5:fc:32:84
    # run cat /sys/class/net/wlan1/address
    command = '/sys/class/net/%s/address' % (int)
    lcd.message('.')
    result = subprocess.run(['cat', command], stdout=subprocess.PIPE).stdout
    macaddress = str(result).strip('b').strip("'")

    if macaddress[:17] == '9c:ef:d5:fc:32:84':
        lcd.message('.')
        interface = int
        return True
    else:
        return False

def startMonitor(interface):
    up = 'ifconfig %s up' % interface
    down = 'ifconfig %s down' % interface
    monitorMode = 'iwconfig %s mode monitor' % interface

    lcd.message('.')
    os.popen(down)
    time.sleep(2)
    lcd.message('.')
    os.popen(monitorMode)
    time.sleep(2)
    lcd.message('.')
    os.popen(up)
    time.sleep(2)
    return True


if __name__ == "__main__":
    with open('/home/pi/code/wifi-probe/config.json') as c:
        config = json.load(c)

    interface = startPi(config)

    interface = interface
    thread = threading.Thread(target=hopper.hopper, args=(interface, ), name="hopper")
    thread.daemon = True
    thread.start()

    sniff(iface=interface, prn=hopper.findSSID, stop_filter=hopper._stop)
