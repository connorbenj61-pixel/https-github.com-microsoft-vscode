import asyncio
import websockets
import json

USERS = {}

async def notify_all(data):
    if USERS:
        msg = json.dumps(data)
        await asyncio.wait([user.send(msg) for user in USERS])

async def send_player_list():
    players = list(USERS.values())
    await notify_all({"type": "player_list", "players": players})

async def handler(websocket, path):
    # Wait for join message with player name
    try:
        join_msg = await websocket.recv()
        join_data = json.loads(join_msg)
        if join_data.get("type") == "join":
            name = join_data.get("name", "Player")
        else:
            name = "Player"
    except Exception:
        name = "Player"
    USERS[websocket] = name
    await send_player_list()
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
            except Exception:
                continue
            if data.get("type") == "chat":
                await notify_all({"type": "chat", "name": USERS[websocket], "msg": data.get("msg", "")})
            elif data.get("type") == "game_event":
                await notify_all({"type": "game_event", "name": USERS[websocket], "event": data.get("event")})
            # Add more event types as needed
    finally:
        USERS.pop(websocket, None)
        await send_player_list()

if __name__ == "__main__":
    start_server = websockets.serve(handler, "0.0.0.0", 8765)
    print("Multiplayer server started on ws://0.0.0.0:8765")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
