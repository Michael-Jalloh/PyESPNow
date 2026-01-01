from pyespnow import EspnowModem
from time import sleep
import json

modem = EspnowModem()
devices = modem.get_ports()
print(devices)
print("===================================")
modem.connect(devices[0]["port"], 115200)
sleep(2)

if modem.new_data:
    data = modem.get_data()
    for i in data:
        d = json.loads(i)
        print(d["msg"])
        print("---------------------------------")
else:
    print("No data")

modem.info()
sleep(2)
if modem.new_data:
    data = modem.get_data()
    for i in data:
        print(i)
        d = json.loads(i)
        print(d["msg"])
        print("---------------------------------")
else:
    print("No data")

modem.version()
sleep(2)
if modem.new_data:
    data = modem.get_data()
    for i in data:
        print(i)
        d = json.loads(i)
        print(d["msg"])
        print("---------------------------------")
else:
    print("No data")

modem.close()
