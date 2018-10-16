##########################################################################################
##########################################################################################
# How to use (python3 knxnetP.py -h to see the usage):
#
# To write a value:
#   python3 knxnetP.py -gwip 127.0.0.1 -gwprt 3671 -a w -v 200 -gadr 3/4/11
#
# To read a value:
#   python3 knxnetP.py -gwip 127.0.0.1 -gwprt 3671 -a r -gadr 4/4/11
#
# Arguments:
#   -gwip/--gateway_ip: Gateway ip
#   -gwprt/--gateway_port: Gateway port
#   -a/--action: "r" to read, "w" to write
#   -v/--value: used only if it is a write action, not required if it is a read action.
#               Accept an int value
#   -gadr/--group_address: Group Address in form x/y/z
##########################################################################################
##########################################################################################

import argparse

from KnxnetProtocol import KnxnetProtocol

parser = argparse.ArgumentParser()
parser.add_argument("-gwip", "--gateway_ip", help="Gateway ip", required=True)
parser.add_argument("-gwprt", "--gateway_port", help="Gateway port", required=True, type=int)
parser.add_argument("-a", "--action", help="write a value to a store or a blind",
                    choices=["r", "w"])
parser.add_argument("-v", "--value", help="Value to write on a store or a blind, not required "
                                          "if it is a read action", type=int)
parser.add_argument("-gadr", "--group_address", help="Group address")

args = parser.parse_args()

gateway_ip = args.gateway_ip
gateway_port = args.gateway_port

data_endpoint = ('0.0.0.0', 3672)
control_endpoint = ('0.0.0.0', 3672)

print("Gateway ip: ", gateway_ip)
print("Gateway port: ", gateway_port)

grp_addr = args.group_address

if args.action == "w":
    value = args.value
    knx = KnxnetProtocol(gateway_ip, gateway_port, 3672, data_endpoint, control_endpoint)
    knx.connect()
    print(args.group_address, " ==> writing ", value)
    knx.write(grp_addr, value)
    knx.disconnect()

if args.action == "r":
    knx = KnxnetProtocol(gateway_ip, gateway_port, 3672, data_endpoint, control_endpoint)
    knx.connect()
    value = knx.read(grp_addr)
    print(args.group_address, " ==> reading ", value)
    knx.disconnect()
