from wifi import Cell, Scheme
import texttable as tt
import time

while(True):
    print("\033c")
    headings = ['ssid','quality','frequency','signal','mode','address','type'];
    table = tt.Texttable()
    table.set_deco(tt.HEADER)
    table.header(headings)

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

        ssidList.append(net.ssid)
        qualityList.append(net.quality)
        frequencyList.append(net.frequency)
        signalList.append(net.signal)
        modeList.append(net.mode)
        addressList.append(net.address)
        typeList.append(enc_type)

        for row in zip(ssidList, qualityList, frequencyList, signalList, modeList, addressList, typeList):
            table.add_row(row)

    wifi_table = table.draw()
    print(wifi_table)

    time.sleep(5)
