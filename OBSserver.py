#!/usr/bin/env python3

import time
import asyncio
import websocket
from datetime import date
import ffmpeg

import win32gui, win32con

import os
import psutil

import ssl
import OBSheader
import json
from obswebsocket import obsws, requests

CURRENT_STATE = "NULL"

class OBS_controller:
    def __init__(self):
        self.obsws = obsws(OBSheader.host, OBSheader.port, OBSheader.password)
        self.obsws.connect()
        self.scene_ids = []
        # self.date = date.today()
        
        self.ws = websocket.WebSocketApp(OBSheader.WBESOCKET_PATH, on_open = self.on_open, on_message = self.on_message, on_error = self.on_error, on_close = self.on_close)

    def handle_command(self, command):
        message = json.loads(command)      
        print(message['command'])    
        if message['command'] == OBSheader.START_RECORDING:            
            
            self.obsws.call(requests.SetFilenameFormatting(OBSheader.RECORDING_FILENAME))     
            
            # Make sure we check the directory exist before setting as our 
            if not os.path.exists(OBSheader.RECORDING_FOLDER):
                os.mkdir(OBSheader.RECORDING_FOLDER)
            self.obsws.call(requests.SetRecordingFolder(OBSheader.RECORDING_FOLDER))  
            
            
            self.obsws.call(requests.StartRecording())    
            CURRENT_STATE = 'Recording'     
            self.dbg("Current State - " + CURRENT_STATE)    
            
        if message['command'] == OBSheader.STOP_RECORDING:
            self.obsws.call(requests.StopRecording())
            CURRENT_STATE = 'Not recording'
            self.dbg("Current State - " + CURRENT_STATE)   
            
            mkv_name = OBSheader.RECORDING_FOLDER + OBSheader.RECORDING_FILENAME + ".mkv"
            mp4_name = OBSheader.RECORDING_FOLDER + OBSheader.RECORDING_FILENAME + ".mp4"
            # input = ffmpeg.input(mkv_name)
            os.system("ffmpeg -i {0} {1}".format(mkv_name, mp4_name))
        
        if message['command'] == OBSheader.STOP_OBS:
            print("Attempting to shut down")
            self.obsws.disconnect()
            for pid in (process.pid for process in psutil.process_iter() if process.name()=="obs64"):
                os.kill(pid)
            exit()
    
    def setup_source(self, source_name, source_kind, scene_name):
        
        # This section is settup up and swtiching to a scene
        self.dbg("Creating scene - " + scene_name)
        self.obsws.call(requests.CreateScene(scene_name))
        self.obsws.call(requests.SetCurrentScene(scene_name))
        
        # Look for the chrome window
        win32gui.EnumWindows(self.winEnumHandler, None )
        
        # Creating a source and switching to it here
        self.dbg("Creating source - " + source_name)
        id = self.obsws.call(requests.CreateSource(source_name, source_kind, scene_name))
        self.dbg("Source ID - " + str(id))
        self.obsws.call(requests.SetSourceSettings(source_name, OBSheader.SOURCE))
        self.scene_ids.append(id)       
    
    def on_message(self, ws, err):
        self.dbg("Received message")
        self.handle_command(err)

    def on_error(self, ws, error):
        self.dbg("Received error - " + str(error))

    def on_close(self, ws, err):
        self.dbg("Connection closed")

    def on_open(self, ws, err):
        self.dbg("Connection opened")

    def dbg(self, dbg_string):
        print(dbg_string)
        f = open(OBSheader.DBG_FILE_PATH + "OBSdbg.txt", "a")
        f.write(dbg_string + "\n")
        f.close()


    def winEnumHandler(self, hwnd, ctx ):
        if 'chrome' in win32gui.GetWindowText( hwnd ).lower():
            self.dbg("FOUND! - " + win32gui.GetWindowText( hwnd ))
            OBSheader.SOURCE = {'window': win32gui.GetWindowText( hwnd ) + ':Chrome_WidgetWin_1:chrome.exe'}


###############################################################################################################################
# Start of the main function 
###############################################################################################################################

async def main():
    # Starting and minimizing OBS
    response = os.startfile(r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\OBS Studio\OBS Studio (64bit).lnk")
    time.sleep(2)
    if response != None:
        exit()
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)
    
    
    # Initializing obs and websocket connection here
    obs_controller = OBS_controller()
    # time.sleep(2)
    obs_controller.setup_source(OBSheader.SOURCE_NAME, OBSheader.SCOURCE_KIND, OBSheader.SCENE_NAME)
    
    #########################################################################################################
    # Connecting to Ismael's server and setting the ssl serts to none. Do we want to do this in production? #
    #########################################################################################################
    # I tried putting this line in the class but it did not work
    # Look into this in the future
    obs_controller.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
    
    while True:
        try:
            obs_controller.dbg("Waiting for message.....")
            result =  ws.recv()
            obs_controller.handle_command(result)
        except Exception as inst:
            obs_controller.dbg("Exception - " + inst)
            obs_controller.ws.close()
            exit()



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())