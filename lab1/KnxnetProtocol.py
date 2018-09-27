import socket
from knxnet import *


class KnxnetProtocol:
    WRITE = 2
    READ = 0

    def __init__(self, gateway_ip, gateway_port, socket_port, data_endpoint, control_endpoint):
        self.gateway_ip = gateway_ip
        self.gateway_port = gateway_port
        self.data_endpoint = data_endpoint
        self.control_endpoint = control_endpoint
        self.socket_port = socket_port
        self.conn_channel_id = 0
        self.sock = None

    def connect(self):
        # -> Socket creation
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('', self.socket_port))

        # -> Sending Connection request
        conn_req_object = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_REQUEST, self.control_endpoint,
                                              self.data_endpoint)
        conn_req_dtgrm = conn_req_object.frame
        # -> Serializing
        self.sock.sendto(conn_req_dtgrm, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection response
        data_recv, addr = self.sock.recvfrom(1024)
        conn_resp_object = knxnet.decode_frame(data_recv)
        if conn_resp_object.status != 0:
            print("Receiving connection response failed")
            return

        # <- Retrieving channel_id from Connection response
        self.conn_channel_id = conn_resp_object.channel_id

        # -> Sending Connection state request
        conn_state_req_obj = knxnet.create_frame(knxnet.ServiceTypeDescriptor.CONNECTION_STATE_REQUEST,
                                                 self.conn_channel_id, self.control_endpoint)
        conn_state_req_dtgram = conn_state_req_obj.frame
        # -> Serializing
        self.sock.sendto(conn_state_req_dtgram, (self.gateway_ip, self.gateway_port))

        # <- Receiving Connection state response
        data_recv, addr = self.sock.recvfrom(1024)
        conn_state_resp_object = knxnet.decode_frame(data_recv)
        if conn_state_resp_object.status:
            print("Receiving connection state response failed")
            return
        print("Connect: OK")

    def disconnect(self):
        # -> Sending Disconnect request
        disconnect_req_obj = knxnet.create_frame(knxnet.ServiceTypeDescriptor.DISCONNECT_REQUEST,
                                                 self.conn_channel_id, self.control_endpoint)
        disconnect_req_dtgram = disconnect_req_obj.frame
        # -> Serializing
        self.sock.sendto(disconnect_req_dtgram, (self.gateway_ip, self.gateway_port))

        # <- Receiving Disconnect response
        data_recv, addr = self.sock.recvfrom(1024)
        disconnect_resp_obj = knxnet.decode_frame(data_recv)
        if disconnect_resp_obj.status:
            print("Disconnect: OK")
        else:
            print("Disconnect: Failed")

    def __action(self, dest_addr_group, acpi, data, data_size):
        if acpi != self.READ and acpi != self.WRITE:
            print("acpi invalide")
            return -1

        # -> Sending Tunnelling request
        dest_addr_group = knxnet.GroupAddress.from_str(dest_addr_group)
        tunnelling_req_obj = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_REQUEST, dest_addr_group,
                                                 self.conn_channel_id, data, data_size, acpi, 0x11)
        tunnelling_req_dtgram = tunnelling_req_obj.frame
        # -> Serializing
        self.sock.sendto(tunnelling_req_dtgram, (self.gateway_ip, self.gateway_port))

        # <- Receiving Tunnelling ack
        data_recv, addr = self.sock.recvfrom(1024)

        # <- Receiving Tunnelling request
        data_recv, addr = self.sock.recvfrom(1024)
        tunnelling_req_obj = knxnet.decode_frame(data_recv)

        # -> Sending Tunnelling ack
        tunnelling_ack_obj = knxnet.create_frame(knxnet.ServiceTypeDescriptor.TUNNELLING_ACK, self.conn_channel_id,
                                                 0, tunnelling_req_obj.sequence_counter)
        tunnelling_ack_dtgram = tunnelling_ack_obj.frame
        # -> Serializing
        self.sock.sendto(tunnelling_ack_dtgram, (self.gateway_ip, self.gateway_port))

        if acpi == self.READ:
            # <- Receiving Tunneling request
            data_recv, addr = self.sock.recvfrom(1024)
            tunnelling_req_obj = knxnet.decode_frame(data_recv)
            return tunnelling_req_obj.data

        return 0

    def read(self, dest_addr_group):
        if dest_addr_group[0] != "4" and dest_addr_group[0] != "0":
            print("Invalid x")
            return
        return self.__action(dest_addr_group, self.READ, 0, 1)

    def write(self, dest_addr_group, data):
        if dest_addr_group[0] != "1" and dest_addr_group[0] != "3" and dest_addr_group[0] != "0":
            print("Invalid x")
            return
        if 0 > data > 255:
            print("Value must be between 0 and 255")
            return
        return self.__action(dest_addr_group, self.WRITE, data, 2)
