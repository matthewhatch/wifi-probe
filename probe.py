from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))

for k,v in networks.iteritems():
    print (k, v)
