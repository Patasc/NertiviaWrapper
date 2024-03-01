import Client
import asyncio

Bot = Client.Client()

with open("token.txt", "r") as file:
    token = file.read()


@Bot.event
async def on_ready(client):
    print("Bot has started !")
    print(client)
    await asyncio.sleep(15)
    await client.close()


@Bot.event
async def on_message(client, message):
    print("Message received !")
    print(message)
    await asyncio.sleep(5)
    print(await message.delete())

Bot.run(token)
