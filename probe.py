from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))
col_width = max(len(word) for row in networks for word in row) + 2

for net in networks:
    print('%s \t %s'%(net.ssid, net.quality)).format(x,x*x)
