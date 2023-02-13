#!/usr/bin/env python3

host = "localhost"
port = 4444
password = "secret"

START_RECORDING = "server_cmd_recording_start"
STOP_RECORDING = "server_cmd_recording_stop"
STOP_OBS = "server_cmd_obs_stop"
DBG_FILE_PATH = "./"
WBESOCKET_PATH = "wss://172.19.16.37:3101?client_type=screen_capture"
SCENE_NAME = "Test Recording"
SCOURCE_KIND = "window_capture"
SOURCE_NAME = "recording"

SOURCE = {"settings":{"window":"obs-websocket/protocol.md at 4.x-compat · obsproject/obs-websocket - Google Chrome:Chrome_WidgetWin_1:chrome.exe"}}

# {"balance":0.5,"deinterlace_field_order":0,"deinterlace_mode":0,"enabled":true,"flags":0,"hotkeys":{},"id":"window_capture","mixers":0,"monitoring_type":0,"muted":false,"name":"recording","prev_ver":486539266,"private_settings":{},"push-to-mute":false,"push-to-mute-delay":0,"push-to-talk":false,"push-to-talk-delay":0,"settings":{"window":"obs-websocket/protocol.md at 4.x-compat · obsproject/obs-websocket - Google Chrome:Chrome_WidgetWin_1:chrome.exe"},"sync":0,"versioned_id":"window_capture","volume":1.0}