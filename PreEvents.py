import Role
import Server
import Person
import Member
import Channel
import Message

import json


async def authenticate(client, cache: dict, data: dict):
    # TODO: Store DMS in client + Implement functions to communicate
    # Unhandled :
    # DMS - lastSeenServerChannels - bannedUserIDs - callingChannelUsersIDs - PID
    # message = data.get("message")

    # Server list empty if not joined any servers ?
    for ServerData in (data["user"]).get("servers", []):
        cache["server_cache"][ServerData["server_id"]] = Server.Server(ServerData, client.header)

    self = Person.Bot(data["user"], client.header)
    cache["user_cache"][data["user"]["id"]] = self
    client.user = self

    for ServerMember in data.get("serverMembers", []):
        isBot = (ServerMember["member"]).get("bot", False)

        cache["user_cache"][ServerMember["member"]["id"]] = Person.User(ServerMember["member"], client.header) if not isBot else Person.Bot(ServerMember["member"], client.header)

    # Sync all of the users status which weo nly obtain via events
    for status in data.get("memberStatusArr", []):
        custom_status = next((value for value in data.get("customStatusArr", []) if value[0] == status[0]), None)
        program_status = next((value for value in data.get("programActivityArr", []) if value[0] == status[0]), None)

        (cache["user_cache"].get(status[0])).update_status({"status": status[1], "custom": custom_status, "game": program_status})

    # Can't have custom emotes so useless (? can't find a way at least)
    del data["settings"]

    for role in data.get("serverRoles", []):
        (cache["server_cache"][role["server_id"]]).add_role(Role.Role(role, client.header))

    for member in data.get("serverMembers", []):
        # FETCH ALL ROLES AND PUT IN LIST THAT MEMBER HAS
        role_list = [
            await (await client.getServer(member["server_id"])).get_role(role_id)
            for role_id in member.get("roles", [])
        ]

        user = cache["user_cache"][member["member"]["id"]]
        server_id = member["server_id"]
        (cache["server_cache"][server_id]).add_member(Member.Member(member, user, role_list, client.header))

    return [client]


async def disconnected(client, cache, data):
    print("Disconnected !")
    print(data)
    return [client]


async def message_received(client, cache, data):
    data = data["message"]
    channelId = data["channelId"]

    channel = None
    for server in (cache["server_cache"]).values():
        tempChannel = server.get_channel(channelId)
        if tempChannel is not None:
            channel = tempChannel

    MessageObject = Message.TextMessage(data, cache, client.header) if data.get("type", 0) == 0 else Message.WelcomeMessage(data, cache, client.header)

    if channel is not None:
        channel.addMessage(MessageObject)

    return [client, MessageObject]
