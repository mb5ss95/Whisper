from .Init import Config
from queue import Queue

import threading
from bluetooth import *

class Ble(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)

            self.DeadOrAlive = True
            self.uuid = Config().get_config("UUID")
            self.evt = threading.Event()
            self.q = Queue()

        def start_Connection(self, client_sock):
            while(self.DeadOrAlive):
                try:
                    data = client_sock.recv(1024)
                    if len(data) == 0:
                        break
                    print("received [%s]"%data)

                    client_sock.send(data[::-1])

                except IOError:
                    print("disconnected")
                    client_sock.close()
                    print("all done")
                    break;
                    
            client_sock.close()

        def DeadOrAlive(self):
            self.DeadOrAlive = False

        def run(self):  
            while(self.DeadOrAlive):
                # RFCOMM Port communication prepare
                server_sock = BluetoothSocket(RFCOMM)
                server_sock.bind(('', PORT_ANY))
                server_sock.listen(1)

                port = server_sock.getsockname()[1]
                
                print(self.uuid)

                # Advertise
                advertise_service(server_sock, "BtChat", service_id = self.uuid, service_classes = [self.uuid, SERIAL_PORT_CLASS], profiles = [SERIAL_PORT_PROFILE])



                print("Waiting for connection : channel %d" % port)

                client_sock, client_info = server_sock.accept()
                print("Accepted connection from ", client_info)

                self.start_Connection(client_sock)
                server_sock.close()