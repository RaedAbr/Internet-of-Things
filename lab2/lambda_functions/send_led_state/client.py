import asyncio
import json
import ssl
import logging

import websockets

async def hello(event):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain('certificate.crt', 'private.key')
    async with websockets.connect(
            'wss://iot-course-master.tk:6789', ssl=ssl_context) as websocket:

        newState = dict(action="led", state=str(event['led_state']))

        await websocket.send(json.dumps(newState))
        print("> {newState}")

        await websocket.recv()
        print(f"< ACK")
        
def lambda_handler(event, context):
    logging.info(event)
    asyncio.run(hello(event))
    print("exit")
    
