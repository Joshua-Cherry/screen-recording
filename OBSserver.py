#!/usr/bin/env python3

import sys
import time
import asyncio
import websocket

import win32gui, win32con

import os
import psutil

import ssl
import OBSheader
import json
from obswebsocket import obsws, requests

CURRENT_STATE = "NULL"


async def main():
    # Starting and minimizing OBS
    response = os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OBS Studio\OBS Studio (64bit).lnk")
    time.sleep(2)
    if response != None:
        dbg("Response from starting OBS: " + response)
        exit()
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    
    
    # Initializing obs and websocket connection here
    obs_controller = OBS_controller()
    time.sleep(2)
    obs_controller.create_scene(OBSheader.SCENE_NAME)
    obs_controller.create_source(OBSheader.SOURCE_NAME, OBSheader.SCOURCE_KIND, OBSheader.SCENE_NAME)
    
    # I tried putting this line in the class but it did not work
    # Look into this in the future
    obs_controller.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    obs_controller.obsws.GetSourcesList()
    
    while True:
        try:
            obs_controller.dbg("Waiting for message.....")
            result =  ws.recv()
            obs_controller.handle_command(result)
        except Exception as inst:
            print("Exception", inst)
            obs_controller.ws.close()
            exit()

class OBS_controller:
    def __init__(self):
        self.obsws = obsws(OBSheader.host, OBSheader.port, OBSheader.password)
        self.obsws.connect()
        self.scene_ids = []
        
        #########################################################################################################
        # Connecting to Ismael's server and setting the ssl serts to none. Do we want to do this in production? #
        #########################################################################################################
        self.ws = websocket.WebSocketApp(OBSheader.WBESOCKET_PATH, on_open = self.on_open, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

    def handle_command(self, command):   
        message = json.loads(command)      
        print(message)    
        if message['command'] == OBSheader.START_RECORDING:
            self.obsws.call(requests.SetFilenameFormatting("TestName"))         
            self.obsws.call(requests.StartRecording()) 
            CURRENT_STATE = 'Recording'         
        if message['command'] == OBSheader.STOP_RECORDING:
            self.obsws.call(requests.StopRecording())
            CURRENT_STATE = 'Not recording'
        if message['command'] == OBSheader.STOP_OBS:
            print("Attempting to shut down")
            # self.ws.close()
            self.obsws.disconnect()
            for pid in (process.pid for process in psutil.process_iter() if process.name()=="obs64"):
                os.kill(pid)
            exit()
            
    def create_scene(self, name):
        self.dbg("Creating scene " + name)
        self.obsws.call(requests.CreateScene(name))
    
    def create_source(self, source_name, source_kind, scene_name):
        self.dbg("Creating source " + source_name)
        id = self.obsws.call(requests.CreateSource(source_name, source_kind, scene_name))
        time.sleep(2)
        self.obsws.call(requests.SetSourceSettings(source_name, source_kind, OBSheader.SOURCE))
        print(self.obsws.call(requests.GetSourceSettings(source_name, source_kind)))
        self.scene_ids.append(id)
        
    
    def on_message(self, message):
        self.dbg("Received message:", message)
        self.handle_command(message)

    def on_error(self, error):
        self.dbg("Received error:", error)

    def on_close(self, err):
        self.dbg("Connection closed")

    def on_open(self, err):
        self.dbg("Connection opened")

    def dbg(self, dbg_string):
        print(dbg_string)
        f = open(OBSheader.DBG_FILE_PATH + "OBSdbg.txt", "a")
        f.write(dbg_string + "\n")
        f.close()




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