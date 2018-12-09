import threading
import os, time
import random

def hopper(iface):
    n = 1
    stop_hopper = False
    while not stop_hopper:
        time.sleep(0.50)
        os.system('iwconfig %s channel %d' % (iface, n))
        print("Current Channel %d" % (n))
        dig = int(random.random() * 14)
        if dig != 0 and dig != n:
            n = dig

if __name__ == "__main__":
    thread = threading.Thread(target=hopper, args=('wlan1mon', ), name="hopper")
    thread.daemon = True
    thread.start()

    while True:
        pass
