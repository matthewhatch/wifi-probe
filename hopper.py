import threading, os, time, random
import Adafruit_CharLCD as LCD
from scapy.all import *

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
lcd.autoscroll = True

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
F_ssids = []    # Founds SSIDs
def findSSID(pkt):
    if pkt.haslayer(Dot11Beacon):
       if pkt.getlayer(Dot11).addr2 not in F_bssids:
           F_bssids.append(pkt.getlayer(Dot11).addr2)

           ssid = pkt.getlayer(Dot11Elt).info
           display_ssid = str(ssid).strip('b').strip("'")

           F_ssids.append(display_ssid)
           if ssid == '' or pkt.getlayer(Dot11Elt).ID != 0:
               print("Hidden Network Detected")
           print("Network Detected: %s - %d networks found" % (display_ssid, len(F_bssids)))
           print(pkt.getlayer(Dot11Elt))
           lcd.clear()
           lcd.message("SSID: %s\nTotal: %d" % (display_ssid, len(F_bssids)))
def _stop(e):
    stop = len(F_bssids) == 20
    if stop:
        lcd.message(' **')
        return stop

def displayFinding():
    lcd.clear()
    lcd.message('Done Collecting')
    time.sleep(2)
    lcd.clear()
    lcd.message('Show Findings...')

    for id in F_ssids:
        time.sleep(2)
        lcd.clear()
        lcd.message('SSID:\n%s' % (id))

if __name__ == "__main__":
    interface = "wlan1mon"
    thread = threading.Thread(target=hopper, args=(interface, ), name="hopper")
    thread.daemon = True
    thread.start()

    sniff(iface=interface, prn=findSSID, stop_filter=_stop, filter='Dot11')
    displayFinding()
