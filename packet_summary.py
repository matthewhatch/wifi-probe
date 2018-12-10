from scapy.all import *

counter = 0

def custom_action(packet):
    global counter
    counter += 1
    # print('couting some shite')
    if packet.haslayer(UDP):
        print(packet.getlayer(UDP).src)
    # print(packet[0][1].dst)
    # return "Packet $s: %s ==> %s" % (counter, packet[0][1].src, packet[0][1].dst)

## Setup sniff, filtering for IP traffic
sniff(filter="ip", prn=custom_action)
