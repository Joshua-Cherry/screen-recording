#!/usr/bin/env python3

import sys
import time
import asyncio
import websockets
import logging
import OBSheader
import json
from obswebsocket import obsws, requests

async def test():
    message = '{ "command": "Stop_Recording", "Data": "Some Data"}'
    x = json.loads(message)
    async with websockets.connect("ws://localhost:8001/") as websocket:
        await websocket.send(message)
        await websocket.close()
        exit()



def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test())



if __name__ == "__main__":    
    main()