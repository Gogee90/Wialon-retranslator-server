import binascii
from socketserver import *

from datetime import datetime

from sqlalchemy.orm import sessionmaker

from wialon.database import Points, engine
from wialon.message_parse import parse_packet

host = 'localhost'
port = int(input('Enter port number: '))
addr = (host, port)


class Server(StreamRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024)
        print('client send: ' + str(self.data))
        parsed_data = parse_packet(binascii.unhexlify(self.data))
        print(parsed_data)
        new_point = Points(device_id=parsed_data['id'],
                           point_time=datetime.fromtimestamp(parsed_data['time']),
                           latitude=parsed_data['params'][b'posinfo']['lat'],
                           longitude=parsed_data['params'][b'posinfo']['lon'],
                           entire_result=str(parsed_data))
        Session = sessionmaker(bind=engine)
        session = Session()
        session.add(new_point)
        session.commit()
        self.request.sendall(b'Success!')


if __name__ == "__main__":
    server = TCPServer(addr, Server)
    print(f'starting server at port {port}')
    server.serve_forever()
