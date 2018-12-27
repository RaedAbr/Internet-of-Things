import asyncio
import json
import logging
from builtins import print

import websockets

logging.basicConfig()

# STATE = {'value': 0}

USERS = set()


# def state_event():
#     return json.dumps({'type': 'state', **STATE})
#
#
# def users_event():
#     return json.dumps({'type': 'users', 'count': len(USERS)})


# async def notify_state():
#     if USERS:       # asyncio.wait doesn't accept an empty list
#         message = state_event()
#         await asyncio.wait([user.send(message) for user in USERS])
#
#
# async def notify_users():
#     if USERS:       # asyncio.wait doesn't accept an empty list
#         message = users_event()
#         await asyncio.wait([user.send(message) for user in USERS])


async def update_led_state(state):
    if USERS:
        message = json.dumps({'type': 'waspmote', 'state': state})
        await asyncio.wait([user.send(message) for user in USERS])


async def register(websocket):
    print("new user")
    USERS.add(websocket)
    # await notify_users()


async def unregister(websocket):
    USERS.remove(websocket)
    # await notify_users()


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        # await websocket.send(state_event())
        async for message in websocket:
            data = json.loads(message)
            if data['action'] == 'led':
                await update_led_state(data["state"])
            else:
                logging.error(
                    "unsupported event: {}", data)
    finally:
        await unregister(websocket)

asyncio.get_event_loop().run_until_complete(websockets.serve(counter, '0.0.0.0', 6789))
asyncio.get_event_loop().run_forever()
