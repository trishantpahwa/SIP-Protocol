from SIP.src.peer.client.client import client
from SIP.src.database.database import database
from SIP.src.packet.request.request import request


class node:

    __client_ = None
    __db = None

    def __init__(self, username, password, client_name, domain,
                 client_network_name, content_type,
                 content_sub_type, protocol='UDP', port='5060'):
        self.__client_ = client(username, password, client_name, domain,
                                protocol, port, client_network_name,
                                content_type, content_sub_type)
        self.__initialize_db()

    def _register_client(self, server_name, server_network_name, server_addr):
        seq_num = '1'  # Random SEQ num
        call_id = '44asdvasdvasdvag435tqw454q34t'  # Random call id
        from_tag = 'asv3442'
        branch = 'branch=asdafsbafb87778878sad;rport'
        protocol = 'UDP'
        request_ = request('REGISTER', self.__client_.get_client_name(),
                           self.__client_.get_domain(),
                           self.__client_.get_protocol(),
                           self.__client_.get_port(), server_name,
                           server_network_name, seq_num, call_id,
                           'register packet', self.__client_.get_content_type(),
                           self.__client_.get_content_sub_type(), from_tag)
        register_packet = request_.get_packet()
        print('Node:\n')
        print(register_packet)
        self.__client_.send_message(register_packet, server_addr)
        print('Ok packet\n')
        ok_packet = self.__client_.receive_message(protocol)
        print(ok_packet)
        self.__client_.disconnect_from_server()

    def _deregister_client(self):
        request_ = request('REGISTER', '999', '999', '192.168.1.218', 'TCP', '6050', '8007', '8007', '1', 'REGISTER', 'application', 'sdp', '123')
        message = request_.get_packet()
        self.__peer_.client_send_message(message)

    # def _establish_session(self):
        # self.__client_.

    def __initialize_db(self):
        self.__db = database('client_data')
        # Might have to add database_tests name
