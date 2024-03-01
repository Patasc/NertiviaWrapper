import asyncio
import json
import websockets

import PreEvents

officialEndpoint = "wss://nertivia.net/socket.io/?EIO=4&transport=websocket"

'''
Get Info of server by ID over HTTP requires to be a member of server else error
'''

PreHandlers = {"on_ready": PreEvents.authenticate, "on_disconnect": PreEvents.disconnected, "on_message": PreEvents.message_received}


class Client:
    # Add an async starting function to allow multiple instances to be ran ?
    def __init__(self):
        self.__token = None
        self.user = None

        self.__user_cache = {}
        self.__server_cache = {}

        self._specialOpcodes = {"0": "40", "2": "3", "40": ""}
        self.handlers = {}
        self.header = {}

        self.__run = False

        self._websocket = None

        with open("Ressources/Events.json", "r") as file:
            self._events = json.load(file)

    async def _send_to_websocket(self, message: str):
        await self._websocket.send(message)

    async def callEvent(self, eventType, payload):
        if eventType in self.handlers.keys():
            cache = {"user_cache": self.__user_cache, "server_cache": self.__server_cache}
            for function in self.handlers[eventType]:
                # Magic trickery
                Args = await PreHandlers[eventType](self, cache, payload)
                await function(*Args)

    async def handleEvent(self, opcode, message):
        # Messy code
        # Don't handle error opcodes such as 41
        if opcode in self._specialOpcodes:
            await self._send_to_websocket(self._specialOpcodes[opcode])

        elif opcode == "42":
            jsonMsg = json.loads(message[2:])
            eventType, payload = self._events[jsonMsg[0]], jsonMsg[1]

            await self.callEvent(eventType, payload)

    async def main(self, endpoint: str = officialEndpoint) -> None:
        loop = asyncio.get_running_loop()

        async with websockets.connect(endpoint) as ws:
            self._websocket = ws
            self.__run = True

            while self.__run:
                try:
                    msg = await self._websocket.recv()

                    opcode = msg[0] if msg[0] != "4" else msg[:2]
                    # Allows to not have to wait for task to finish
                    loop.create_task(self.handleEvent(opcode, msg))

                except websockets.ConnectionClosedOK:
                    print("Websocket correctly closed")
                    self.__run = False
                except websockets.ConnectionClosedError:
                    print("Unexpected error\tWebsocket closed")
                    self.__run = False

            await ws.close()

    def run(self, token):
        # Maybe return True if closed properly, else False
        self.__token = token
        self._specialOpcodes["40"] = "42" + json.dumps(["authentication", {"token": token}])
        self.header = {"Authorization": token, "Content-Type": "Application/json"}

        try:
            asyncio.run(self.main())
        except RuntimeError:
            # TODO: Probs need to fix this caused by asyncio.stop() without returning a future
            pass

    async def getUser(self, userId: str):
        return self.__user_cache.get(userId)

    async def getServer(self, serverId: str):
        return self.__server_cache.get(serverId)

    def event(self, function):
        # TODO: Make a handler for every type to be called before execution of function to cache + format args
        if not asyncio.iscoroutinefunction(function):
            raise TypeError(f"Wrapper applied at {function.__name__} which is not a coroutine")

        if function.__name__ not in self.handlers.keys():
            self.handlers[function.__name__] = []

        self.handlers[function.__name__].append(function)

        def inner(*args):
            return function(*args)

        return inner

    async def close(self):
        # Brutal way of closing -- TODO: Rewrite for cleaner code
        # loop = asyncio.get_event_loop()
        # loop.stop()
        self.__run = False
