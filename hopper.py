import threading, os, time, random
import Adafruit_CharLCD as LCD
from scapy.all import *
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

def hopper(iface):
    n = 1
    stop_hopper = False
    while not stop_hopper:
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))
        dig = int(random.random() * 14)
        if dig != 0 and dig != n:
            n = dig

F_bssids = []    # Found BSSIDs
F_unsecure = []    # Founds SSIDs

def findSSID(pkt):
    if pkt.haslayer(Dot11Beacon):
       if pkt.getlayer(Dot11).addr2 not in F_bssids:
           F_bssids.append(pkt.getlayer(Dot11).addr2)
           bssid = pkt.getlayer(Dot11).addr2
           ssid = pkt.getlayer(Dot11Elt).info
           signal_strength = getSignalStrength(pkt)
           # distance = getDistance(signal_strength)
           display_ssid = str(ssid).strip('b').strip("'")
           crypto = getEncryptionType(pkt)
           print("Network Detected: %s %s %s %s" % (display_ssid, ' / '.join(crypto), signal_strength, bssid))
           if 'WEP' in crypto or 'OPN' in crypto:
               F_unsecure.append(display_ssid)
               if ssid == '' or pkt.getlayer(Dot11Elt).ID != 0:
                   print("Hidden Network Detected")
               lcd.clear()
               lcd.message('Insecure Network\nDetected!')
               time.sleep(1)

           lcd.clear()
           lcd.message('Total Found: %d\nInsecure: %d' % (len(F_bssids), len(F_unsecure)))

def _stop(e):
    with open('/home/pi/code/wifi-probe/config.json') as c:
        config = json.load(c)

    stop = len(F_bssids) == config["totalCount"]
    if stop:
        lcd.message(' **')
        return stop

def getEncryptionType(pkt):
    p = pkt[Dot11Elt]
    cap = pkt.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}"
                      "{Dot11ProbeResp:%Dot11ProbeResp.cap%}").split('+')
    crypto = set()
    while isinstance(p, Dot11Elt):
        if p.ID == 48:
            crypto.add("WPA2")
        elif p.ID == 221 and str(p.info).startswith('\x00P\xf2\x01\x01\x00'):
            crypto.add("WPA")
        p = p.payload
    if not crypto:
        if 'privacy' in cap:
            crypto.add("WEP")
        else:
            crypto.add("OPN")
    return crypto

def getSignalStrength(pkt):
    if pkt.haslayer(RadioTap):
        radio_tap = pkt.getlayer(RadioTap)
        return -(256-ord(pkt.notdecoded[-4:-3]))

def getDistance(db):
    return pow(10., (-34. -(db))/(10*4))
