from KnxnetProtocol import *

gateway_ip = "127.0.0.1"
gateway_port = 3671

# -> in this example, for sake of simplicity, the two ports are the same
# With the simulator, the gateway_ip must be set to 127.0.0.1 and gateway_port to 3671

data_endpoint = ('0.0.0.0', 3672)
control_endpoint = ('0.0.0.0', 3672)

knx = KnxnetProtocol(gateway_ip, gateway_port, 3672, data_endpoint, control_endpoint)
knx.connect()
print(knx.write("3/4/11", 130))

