from seriallink import get_ports
from serial import Serial
from threading import Thread
import json
from threading import Thread

class EspnowModem:

    def __init__(self, debug = False, name = "node-01"):
        self.conn = None
        self.new_data = False
        self.data = []
        self.running = True
        self.debug = debug
        self.name = name

    def get_ports(self, devices="USB"):
        ports = get_ports(devices)
        return ports
    
    def connect(self, port, baudrate, timeout=1.0):
        self.conn = Serial(port, baudrate, timeout=timeout)
        self.help()
        t = Thread(target=self.run)
        t.daemon = True
        t.start()

    def get_data(self):
        if self.new_data:
            self.new_data = False
            data = [i for i in self.data]
            self.data = []
            return data
        return None
    
    def run(self):
        try:
            while self.running:
                if self.conn:
                    data = self.conn.readline()
                    if data:
                        self.data.append(data.replace(b"\r\n",b""))
                        self.new_data = True
        except Exception as e:
            print(str(e))
    
    def send(self, data):
        if self.debug:
            print(data)
        if self.conn:
            data = json.dumps(data)
            data += "\r\n"
            self.conn.write(data.encode("utf-8"))
            if self.debug:
                print("Sent")
    
    def broadcast(self, message):
        cmd = {"cmd":"broadcast","msg":message}
        self.send(cmd)
    
    def send_message(self, message, address):
        cmd = {"cmd":"send", "msg":message, "address": address}
        self.send(cmd)
        
    def help(self):
        cmd = {"cmd":"help"}
        self.send(cmd)
    
    def set_name(self, name =""):
        if name:
            self.name = name
        cmd = {"cmd":"name","data":self.name}
        self.send(cmd)
    
    def info(self):
        cmd = {"cmd":"info"}
        self.send(cmd)
    
    def version(self):
        cmd = {"cmd":"version"}
        self.send(cmd)

    def close(self):
        self.conn.close()
