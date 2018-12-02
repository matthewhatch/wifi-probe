from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for net in networks:
    print('%s \t %s'%(net.ssid, net.quality)).format(x,x*x)
