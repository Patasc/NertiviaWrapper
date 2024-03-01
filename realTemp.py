import websockets
import json
import asyncio

url = "wss://nertivia.net/socket.io/?EIO=4&transport=websocket"

with open("token.txt", "r") as file:
    token = file.read()

# https://github.com/socketio/engine.io/blob/master/lib/parser-v3/index.ts
# found in engineio doc :
resp = {"open": 0, "close": 1, "ping": 2, "pong": 3, "message": 4, "upgrade": 5, "noop": 6}
import requests


async def run():
    async with websockets.connect(url) as ws:
        run = True
        c = None
        while run:
            try:
                message = await ws.recv()
                print(message)

                if message[0] == "0":
                    await ws.send("40")

                elif message[:2] == "40":
                    c = json.loads(message[2:])["sid"]
                    print('42["authentication", {"token" : "' + token + '"}]')
                    await ws.send('42["authentication", {"token" : "' + token + '"}]')
                elif message[:2] == "42":

                    r = requests.get("https://nertivia.net/api/user/6904829056001249280", headers={"Cookie": f"connect.sid={c}", "authorization": token})
                    print(r.content)

                elif message == "2":
                    print("Ping")
                    await ws.send("3")
                    print("Pong")
            except websockets.ConnectionClosedError:
                print("Err")
                run = False
            except websockets.ConnectionClosed:
                run = False
                print("Con closed")

asyncio.run(run())
