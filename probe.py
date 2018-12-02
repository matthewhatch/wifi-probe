from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for net in networks:
    enc_type = net.encryption_type if net.encrypted else 'open'
    print(net.ssid, net.quality, net.frequency, net.signal, net.mode, net.address, enc_type)
