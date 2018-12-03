from wifi import Cell, Scheme
import texttable as tt
import sys
import time

while(True):
    os.system('clear')
    headings = ['ssid','quality','frequency','signal','mode','address','type'];
    tab = tt.Texttable()
    tab.header(headings)

    networks = list(Cell.all('wlan0'))
    for net in networks:
        # set up the tabl
        ssidList = list()
        qualityList = list()
        frequencyList = list()
        signalList = list()
        modeList = list()
        addressList = list()
        typeList = list()

        enc_type = net.encryption_type if net.encrypted else 'open'
        # print(net.ssid, net.quality, net.frequency, net.signal, net.mode, net.address, enc_type)
        ssidList.append(net.ssid)
        qualityList.append(net.quality)
        frequencyList.append(net.frequency)
        signalList.append(net.signal)
        modeList.append(net.mode)
        addressList.append(net.address)
        typeList.append(enc_type)

        for row in zip(ssidList, qualityList, frequencyList, signalList, modeList, addressList, typeList):
            tab.add_row(row)

    wifi_table = tab.draw()
    sys.stdout(wifi_table)
    sys.stdout.flush()
    time.sleep(5)
