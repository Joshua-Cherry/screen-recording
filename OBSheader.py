#!/usr/bin/env python3

host = "localhost"
port = 4444
password = "secret"

START_RECORDING = "server_cmd_obs_start"
STOP_RECORDING = "server_cmd_obs_stop"
STOP_OBS = "server_cmd_obs2_stop"

DBG_FILE_PATH = "./"
WBESOCKET_PATH = "wss://172.19.16.37:3101?client_type=screen_capture"
SCENE_NAME = "Test Recording"
SCOURCE_KIND = "window_capture"
SOURCE_NAME = "recording"

SOURCE =  {'window':'(1) Alley-oops but they get increasingly more insane - YouTube - Google Chrome:Chrome_WidgetWin_1:chrome.exe'}
# {"window":"(1) Khem Birch Is A Good Pickup? - YouTube - Google Chrome:Chrome_WidgetWin_1:chrome.exe"}
# {"window":"websocket-client · PyPI - Google Chrome:Chrome_WidgetWin_1:chrome.exe"}
# {"window":"(1) Breaking Ned (Breaking Bad x The Simpsons) - YouTube - Google Chrome:Chrome_WidgetWin_1:chrome.exe"}
# {"window":"(1) Alley-oops but they get increasingly more insane - YouTube - Google Chrome:Chrome_WidgetWin_1:chrome.exe"}
