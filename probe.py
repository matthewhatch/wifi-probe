from wifi import Cell, Scheme

networks = list(Cell.all('wlan0'))
print('ssid\tquality')
for net in networks:
    print(f'{net.ssid}\t {net.quality}')
