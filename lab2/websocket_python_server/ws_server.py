import asyncio
import json
import logging
import logging.config
import os
import ssl
import sys
from builtins import print

import websockets


async def broadcast_led_state(state):
    logging.debug(f"broadcast state")
    message = json.dumps({'type': 'led', 'state': state})
    logging.info(f"> broadcast message: {message}")
    if clients_list:
        await asyncio.wait([user.send(message) for user in clients_list])


async def broadcast_desired_led_state(state):
    logging.debug(f"broadcast desired state")
    message = json.dumps({'type': 'pending', 'desiredState': state})
    logging.info(f"> broadcast message: {message}")
    if clients_list:
        await asyncio.wait([user.send(message) for user in clients_list])


async def broadcast_last_temp(temp, time):
    logging.debug(f"broadcast last temperature")
    message = json.dumps({'type': 'temp', 'temp': temp, 'time': time})
    logging.info(f"> broadcast message: {message}")
    if clients_list:
        await asyncio.wait([user.send(message) for user in clients_list])


async def broadcast_accelero_state(x_acc, y_acc, z_acc, time):
    logging.debug(f"broadcast last accelerometer values")
    message = json.dumps({
        'type': 'accelero',
        'x_acc': x_acc,
        'y_acc': y_acc,
        'z_acc': z_acc,
        'time': time
    })
    if clients_list:
        await asyncio.wait([user.send(message) for user in clients_list])


async def broadcast_ack():
    message = "ACK"
    if clients_list:
        await asyncio.wait([user.send(message) for user in clients_list])


async def register(websocket):
    logging.debug(f"register new user {websocket.remote_address}")
    clients_list.add(websocket)
    logging.info(f"new client {websocket.remote_address} registred")


async def unregister(websocket):
    logging.debug(f"unregister user {websocket.remote_address}")
    clients_list.remove(websocket)
    logging.info(f"client {websocket.remote_address} unregistred")


async def handler(websocket, path):
    logging.debug(f"websocket handler called by client {websocket.remote_address}")
    await register(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            logging.info(f"< message recieved: {data} from {websocket.remote_address}")
            if data['action'] == 'led':
                await broadcast_led_state(data["state"])
            elif data['action'] == 'requestState':
                await broadcast_desired_led_state(data['state'])
            elif data['action'] == 'temp':
                await broadcast_last_temp(data['temp'], data['time'])
            elif data['action'] == 'accelero':
                await broadcast_accelero_state(data['x_acc'], data['y_acc'], data['z_acc'], data['time'])
            else:
                logging.error("unsupported event: {}", data)
                await broadcast_ack()
    finally:
        await unregister(websocket)


############################################
# main program
############################################

# ----------- logger config -----------
# default logging level
numeric_level = logging.INFO
# for other logging level
if len(sys.argv) > 1:
    loglevel = sys.argv[1]
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        print(f"Invalid argument: {loglevel}\n")
        print(f"Usage\t{sys.argv[0]} [DEBUG|INFO|CRITICAL|ERROR|WARNING]")
        exit(1)
logging.basicConfig(
    # filename="server.log",
    level=numeric_level,
    format="%(asctime)s - %(levelname)s: %(message)s"
)
# ----------- ssl config -------------
current_dir = os.path.dirname(os.path.realpath(__file__))
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.check_hostname = False
ssl_context.load_cert_chain(current_dir + '/certificate.crt', current_dir + '/private.key')
logging.debug(f"ssl context OK")
# ----------- create websocket server -----------
PORT = 6789
socket = websockets.serve(handler, '0.0.0.0', PORT, ssl=ssl_context)
logging.info(f"server listening on port {PORT} (wss protocol)...")
# ----------- connected clients list -----------
clients_list = set()

asyncio.get_event_loop().run_until_complete(socket)
asyncio.get_event_loop().run_forever()
