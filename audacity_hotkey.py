#!/usr/bin/env python

import os
import sys
import time
from pynput import keyboard
import win32clipboard
from io import BytesIO

if sys.platform == 'win32':
    TONAME = '\\\\.\\pipe\\ToSrvPipe'
    FROMNAME = '\\\\.\\pipe\\FromSrvPipe'
    EOL = '\r\n\0'
else:
    TONAME = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
    FROMNAME = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
    EOL = '\n'

if not os.path.exists(TONAME):
    print(TONAME, " does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

if not os.path.exists(FROMNAME):
    print(FROMNAME, "does not exist.  Ensure Audacity is running with mod-script-pipe.")
    sys.exit()

print("")
TOFILE = open(TONAME, 'w')
FROMFILE = open(FROMNAME, 'rt')

def send_command(command):
    TOFILE.write(command + EOL)
    TOFILE.flush()

def get_response():
    result = ''
    line = ''
    while True:
        result += line
        line = FROMFILE.readline()
        if line == '\n' and len(result) > 0:
            break
    return result

def do_command(command):
    send_command(command)
    response = get_response()
    return response


# Custom command functions 
def delete_all_tracks():
    do_command("SelAllTracks:")
    do_command("RemoveTracks:")

def trim():
    do_command("Trim:")
    do_command("Align_StartToZero::")

def start_recording():
    do_command("Record2ndChoice:")

def stop_recording():
    do_command("Stop:")

def export():
    do_command("ExportMp3:")    

def delete_file(file):
    try:
        os.remove(file)
    except OSError as e:
        print(e)

# Create Hotkey
recording = False
current = set()
key_toggle_record = keyboard.Key.f10
key_trim_export = keyboard.Key.f9
filename = 'untitled.mp3'
path = os.path.join(filename)
hotkeys = [key_toggle_record, key_trim_export]

def execute(key):
    global recording
    if key == key_toggle_record:
        if recording:
            recording = False
            stop_recording()
        else:
            delete_all_tracks()
            recording = True
            start_recording()

    if key == key_trim_export:
        delete_file(path) # delete existing file if it exists
        trim()
        export()

def on_press(key):
    if key in hotkeys:
        execute(key)

if __name__ == '__main__':
    with keyboard.Listener(on_press=on_press) as listener:
       listener.join()

