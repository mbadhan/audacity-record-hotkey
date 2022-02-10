# audacity-record-hotkey
Python script to configure hotkeys for quick desktop audio recording and exporting. Needs Audacity open before running the script. 

By default, pressing F10 will remove all tracks and start recording a new track. 
Pressing F9 will take the current selection, trim the track so it consists of just that section, and then export it as an mp3 file. 

Audacity scripting boilerplate taken from: https://github.com/audacity/audacity/blob/master/scripts/piped-work/pipe_test.py
