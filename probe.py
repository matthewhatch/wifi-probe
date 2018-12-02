from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for net in networks:
    print('%s \t %s'.format(net,net*net))%(net.ssid, net.quality)
