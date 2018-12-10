import threading, os, time, random
import Adafruit_CharLCD as LCD
import time
import subprocess

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

def startPi():
    i=0
    started = False
    message = 'Starting Wifi\nHopper.'
    lcd.clear()
    lcd.message('Welcome to\nPi Scanner')
    time.sleep(5)
    lcd.clear()
    lcd.message(message)
    while started != True:
        #lcd.clear()
        # lcd.message(message)
        lcd.message('.')
        if i < 4:
            i += 1
        else:
            i = 0
            lcd.clear()
            lcd.message(message)
        started = isMonitor('wlan%d' % (i-1))
        print('started value is %s' % started)
        time.sleep(.5)
    lcd.clear()
    startMonitor('wlan%d' % (i-1))
    lcd.clear()
    lcd.message('starting monitor\nmode')
    time.sleep(5)
    lcd.clear()
    startHopper()
    lcd.message('Hoppah\nstahted!')

def isMonitor(interface):
    # we need to determine what Network card is
    # 9c:ef:d5:fc:32:84
    # run cat /sys/class/net/wlan1/address
    command = '/sys/class/net/%s/address' % (interface)
    print('checking %s' % (command))
    result = subprocess.run(['cat', command], stdout=subprocess.PIPE).stdout
    macaddress = str(result).strip('b').strip("'")
    print('result: %s' % (macaddress[:17]))
    if macaddress[:17] == '9c:ef:d5:fc:32:84':
        return True
    else:
        return False

def startMonitor(interface):
    command = 'start %s' % interface
    subprocess.run(['airmon-ng', command], stdout=subprocess.PIPE)
    return True

def startHopper():
    command = '/home/pi/code/wifi-probe/hopper.py'
    subprocess.run(['python3', command], stdout=subprocess.PIPE)
    return True

if __name__ == "__main__":
    startPi()
