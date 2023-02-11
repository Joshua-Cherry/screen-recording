#!/usr/bin/env python3

import sys
import time
import asyncio
import websockets
import logging
import OBSheader
import json
from obswebsocket import obsws, requests

async def main():
    try:
        stop = asyncio.Future()
        async with websockets.serve(handler, "", 8001):
            await stop # run forever

            print("End of list")

    except KeyboardInterrupt:
        pass

    
async def handler(websocket, path):

    ws = obsws(OBSheader.host, OBSheader.port, OBSheader.password)
    sc = scene_controller()._init_("NULL")
    
    ws.connect()

    while True:
        async for message in websocket:
            try:            
                print(message)
                command = json.loads(message)
                print(command['command'])
                if command['command'] == OBSheader.START_RECORDING:
                    ws.call(requests.StartRecording())                        
                if command['command'] == OBSheader.STOP_RECORDING:
                    ws.call(requests.StopRecording())
                if command['command'] == OBSheader.STOP_SERVER:
                    print("Attempting to shut down")
                    ws.disconnect()
                    exit()
            except Exception as ex:
                print(ex)
                ws.disconnect()
                exit()

class scene_controller():
    def _init_(self, name):
        self.name = name
    
    def create_scence(self, ws, requests, name):
        ws.call(requests.CreateScene(name))



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())