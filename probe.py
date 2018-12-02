from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for net in networks:
    print('%s \t %s'.format(x,x*x))%(net.ssid, net.quality)
