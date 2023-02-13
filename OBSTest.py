#!/usr/bin/env python3

import sys
import time
import asyncio
import websockets
import websocket
import logging
import OBSheader
import json
from obswebsocket import obsws, requests

async def test():
    message = '{ "command": "server_cmd_stop_obs", "Data": "Some Data"}'
    
    ws = websocket.WebSocketApp("wss://172.19.16.37:3101?client_type=screen_capture")
    ws.send(message)
    ws.close()
    # x = json.loads(message)
    # async with websockets.connect("wss://172.19.16.37:3101?client_type=screen_capture") as websocket:
    #     await websocket.send(message)
    #     await websocket.close()
    #     exit()



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())



if __name__ == "__main__":    
    main()