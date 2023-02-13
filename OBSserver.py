#!/usr/bin/env python3

import sys
import time
import asyncio
import websocket
from websocket import create_connection
import ssl
import logging
import OBSheader
import json
from obswebsocket import obsws, requests

CURRENT_STATE = "NULL"


def on_message(ws, message):
    print("Received message:", message)
    handle_command(ws, message)

def on_error(ws, error):
    print("Received error:", error)

def on_close(ws):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")


async def main():

    # ws = create_connection("wss://172.19.16.37:3101?client_type=screen_capture", sslopt={"cert_reqs": ssl.CERT_NONE})
    ws = websocket.WebSocketApp("wss://172.19.16.37:3101?client_type=screen_capture", on_open = on_open, on_message = on_message, on_error = on_error, on_close = on_close)
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    # ws.send("Hello, World")
    # print("Sent")
    # print("Receiving...")
    # while True:
    #     try:
    #         result =  ws.recv()
    #         handle_command(result)
    #     except Exception as inst:
    #         print("Exception", inst)
    #         ws.close()
    #         exit()

    
    # try:
    #     # stop = asyncio.Future()
    #     async with websockets.connect("wss://172.19.16.37:3101?client_type=screen_capture", sslopt={"cert_reqs": ssl.CERT_NONE}) as wbsc:
    #         # await stop # run forever
    #         while true:
    #             res = wbsc.rec(v)
    #             print(res)

    # except KeyboardInterrupt:
    #     exit()

def handle_command(ws, command):   
    OBSWS = obsws(OBSheader.host, OBSheader.port, OBSheader.password)
    
    OBSWS.connect()
         
    message = json.loads(command)      
    print(message)    
    if message['command'] == OBSheader.START_RECORDING:
        OBSWS.call(requests.SetFilenameFormatting("TestName"))         
        OBSWS.call(requests.StartRecording()) 
        CURRENT_STATE = 'Recording'         
    if message['command'] == OBSheader.STOP_RECORDING:
        OBSWS.call(requests.StopRecording())
        CURRENT_STATE = 'Not recording'
    if message['command'] == OBSheader.STOP_OBS:
        print("Attempting to shut down")
        # ws.close()
        OBSWS.disconnect()
        # exit()

    
# async def handler(websocket, path):

#     ws = obsws(OBSheader.host, OBSheader.port, OBSheader.password)
    
#     ws.connect()

#     while True:
#         async for message in websocket:
#             try:            
#                 command = json.loads(message)          
#                 if command['command'] == OBSheader.START_RECORDING:
#                     ws.call(requests.SetFilenameFormatting("TestName"))         
#                     ws.call(requests.StartRecording())          
#                 if command['command'] == OBSheader.STOP_RECORDING:
#                     ws.call(requests.StopRecording())
#                 if command['command'] == OBSheader.STOP_SERVER:
#                     print("Attempting to shut down")
#                     ws.disconnect()
#                     exit()
#             except Exception as ex:
#                 print(ex)
#                 ws.disconnect()
#                 exit()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())