import socket
import sys
from time import sleep

from zeroconf import ServiceInfo, Zeroconf

TYPE = "_http._tcp.local."
NAME = "waker"

class Waker:
    def __init__(self, port):
        hostname = socket.gethostname()
        desc = {'name': hostname}

        self.hostip = self.get_ip()
        self.port = port
        self.info = ServiceInfo(TYPE,
                                "{}.{}".format(NAME, TYPE),
                                socket.inet_aton(self.hostip), port, 0, 0,
                                desc)
        self.zeroconf = Zeroconf()

    def get_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        return s.getsockname()[0]

    def register(self):
        print("Registering {}.{} with avahi at {}:{}".format(NAME, TYPE, self.hostip, self.port))

        self.zeroconf.register_service(self.info)

    def unregister(self):
        self.zeroconf.unregister_service(self.info)
        self.zeroconf.close()
