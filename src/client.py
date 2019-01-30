import socket

import transfer_server
import transfer_client
import request_packet
import payload
import database


class client:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    buff_size = 4096
    db = None

    client_name = ''
    domain = ''
    protocol = ''
    port = 6050
    client_network_name = ''
    server_network_name = ''
    server_name = ''
    content_type = ''
    content_sub_type = ''
    tag = 123

    client_addr = (socket.gethostbyname(socket.gethostname()), port)

    def __init__(self, client_name, domain, protocol, port, client_network_name, server_network_name, server_name, content_type, content_sub_type):
        self.server_name = server_name
        self.domain = domain
        self.protocol = protocol
        self.port = port
        self.client_network_name = client_network_name
        self.server_network_name = server_network_name
        self.client_name = client_name
        self.content_type = content_type
        self.content_sub_type = content_sub_type
        self.db = database.database()
        self.connect_to_server(1)

    def send_file(self, server_addr, file_name):
        c = transfer_client.transfer_client(server_addr)
        c.get_file(file_name)

    def recv_file(self, file_type, extension):
        t = transfer_server.transfer_server(file_type, extension)
        t.save_file(file_type, file_data, extension)

    def connect_to_server(self, seq_num):
        self.s.connect(self.client_addr)
        register_packet = self.register_client(seq_num)
        seq_num += 1
        self.send_message(register_packet)
        packet = self.s.recv(self.buff_size).decode('UTF-8')
        print(packet)
        print(' ')
        self.establish_session(seq_num, socket.gethostbyname(socket.gethostname()), 'audio')

    def establish_session(self, seq_num, destination_client_ip, media_type):
        self.db.display_data({'client_name': 'CLIENT1', 'client_network_name': 'client1'})
        invite_packet = self.invite(1) #seq_num here
        self.send_message(invite_packet)
        print('Sent invite packet')
        payload = self.payload(destination_client_ip, media_type)
        self.send_message(payload)
        print('Sent payload')

        '''trying_packet = self.s.recv(self.buff_size).decode('UTF-8')
        print(trying_packet)
        print('')
        ringing_packet = self.s.recv(self.buff_size).decode('UTF-8')
        print(ringing_packet)
        print('')
        ok_packet = self.s.recv(self.buff_size).decode('UTF-8')
        print(ok_packet)
        print('')
        ack_packet = self.ack(4) #seq_num here
        self.send_message(ack_packet)
        print('Sent ack packet')
        payload = self.payload(destination_client_ip, media_type)
        self.send_message(payload)
        print('Sent payload')'''

    def send_message(self, message):
        self.s.send(message.encode('UTF-8'))

    def register_client(self, seq_num):
        r = request_packet.request_packet(3, self.client_name, self.domain, self.protocol, self.port, self.client_network_name, self.server_network_name, self.server_name, seq_num, 'Register client', self.content_type, self.content_sub_type)
        packet = r.get_packet()
        return packet

    def invite(self, seq_num):
        r = request_packet.request_packet(1, self.client_name, self.domain, self.protocol, self.port, self.client_network_name, self.server_network_name, self.server_name, seq_num, 'INVITE', self.content_type, self.content_sub_type)
        packet = r.get_packet()
        return packet

    def ack(self, seq_num):
        r = request_packet.request_packet(4, self.client_name, self.domain, self.protocol, self.port, self.client_network_name, self.server_network_name, self.server_name, seq_num, 'ACK', self.content_type, self.content_sub_type)
        packet = r.get_packet()
        return packet

    def payload(self, destination_client_ip, media_type):
        p = payload.payload(self.client_name, self.domain, destination_client_ip, media_type)
        p = p.get_payload()
        return p

    def bye(self, seq_num):
        r = request_packet.request_packet(2, self.client_name, self.domain, self.protocol, self.port, self.client_network_name, self.server_network_name, self.server_name, seq_num, 'BYE', self.content_type, self.content_sub_type)
        packet = r.get_packet()
        return packet