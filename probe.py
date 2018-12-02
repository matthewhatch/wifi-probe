from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for net in networks:
    print(net.ssid, net.quality, net.frequency, net.signal, net.mode, net.address, net.encrypted, net.encryption_type)
