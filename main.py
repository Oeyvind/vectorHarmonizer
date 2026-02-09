#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Vector harmonize server, receive notes and control data via OSC, generate notes and return those on OSC

@author: Øyvind Brandtsegg
@contact: obrandts@gmail.com
@license: GPL
"""

from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
from osc4py3 import oscmethod as osm
import time, threading
import vectorHarmonizeWrapper
vhWrap = vectorHarmonizeWrapper.VectorHarmWrap()

receive_address = '127.0.0.1', 8910
send_address = '127.0.0.1', 8912

osc_startup()

osc_udp_server(receive_address[0], receive_address[1], "vectorHarmServer")
osc_udp_client(send_address[0], send_address[1], "vectorHarmClient")
print(receive_address)

# message handlers
def note_handler(addr, note,velocity,chan):
    harmnote = 0
    if vhWrap.playChannels[chan-1]:
        while harmnote > -999:
            if velocity > 0:
                harmnote, fracinstr = vhWrap.vectorHarmonizeMidiNote(note, chan, 0)
            else:
                pass
                harmnote, fracinstr = vhWrap.vectorHarmonizeMidiNoteOff(note, chan)
            if harmnote > -999:
                returnmsg = [harmnote, velocity, chan, fracinstr]
                print(returnmsg)
                msg = oscbuildparse.OSCMessage("/vectorHarmonizerReturnNote", None, returnmsg)
                osc_send(msg, "vectorHarmClient")
        if vhWrap.vectorHarmonizeAutoVoiceRange:
            low, high = vhWrap.getVectorHarmonizeVoiceRange()
            rangemsg = [low,high]
            msg = oscbuildparse.OSCMessage("/vectorHarmonizerControlReturn/range", None, rangemsg)
            osc_send(msg, "vectorHarmClient")
    if vhWrap.recordChannels[chan-1] and velocity > 0:
        vector = vhWrap.recordIntervalVector(note)
        if vector != None:
            msg = oscbuildparse.OSCMessage("/vectorHarmonizerControlReturn/vector", None, vector)
            osc_send(msg, "vectorHarmClient")

def control_handler(addr, value):

    if addr == "/vectorHarmonizerControl/play1":
        vhWrap.playChannels[0] = int(value)
    if addr == "/vectorHarmonizerControl/play2":
        vhWrap.playChannels[1] = int(value)
    if addr == "/vectorHarmonizerControl/play3":
        vhWrap.playChannels[2] = int(value)
    if addr == "/vectorHarmonizerControl/play4":
        vhWrap.playChannels[3] = int(value)
    if addr == "/vectorHarmoizerControl/play5":
        vhWrap.playChannels[4] = int(value)
    if addr == "/vectorHarmonizerControl/record1":
        vhWrap.recordChannels[0] = int(value)
    if addr == "/vectorHarmonizerControl/record2":
        vhWrap.recordChannels[1] = int(value)
    if addr == "/vectorHarmonizerControl/record3":
        vhWrap.recordChannels[2] = int(value)
    if addr == "/vectorHarmonizerControl/record4":
        vhWrap.recordChannels[3] = int(value)
    if addr == "/vectorHarmonizerControl/record5":
        vhWrap.recordChannels[4] = int(value)

    if addr == "/vectorHarmonizerControl/auto_vRange":
        vhWrap.vectorHarmonizeAutoVoiceRange = int(value)
    if addr == "/vectorHarmonizerControl/kvRangeMin":
        vhWrap.vHarmonize.voiceRange[0] = int(value)
    if addr == "/vectorHarmonizerControl/kvRangeMax":
        vhWrap.vHarmonize.voiceRange[1] = int(value)
    if addr == "/vectorHarmonizerControl/krthresh":
        vhWrap.setPcsetRecordThreshTime(value)
    if addr == "/vectorHarmonizerControl/kvRangeBorder":
        vhWrap.vHarmonize.autoVoiceRangeBorder = value
    if addr == "/vectorHarmonizerControl/kvRangeScore":
        vhWrap.vHarmonize.voiceRangeScore = value
    if addr == "/vectorHarmonizerControl/kgravityScore":
        vhWrap.vHarmonize.voiceRangeGravity = value
    if addr == "/vectorHarmonizerControl/kcommonScore":
        vhWrap.vHarmonize.commonToneScore = value
    if addr == "/vectorHarmonizerControl/kdistanceScore":
        vhWrap.vHarmonize.distanceScore = value
    if addr == "/vectorHarmonizerControl/kparallelScore":
        vhWrap.vHarmonize.parallelMotionScore = value
    if addr == "/vectorHarmonizerControl/kspreadScore":
        vhWrap.vHarmonize.voiceSpreadScore = value
    if addr == "/vectorHarmonizerControl/ktoggleScore":
        vhWrap.vHarmonize.chordToggleScore = value
    if addr == "/vectorHarmonizerControl/krepeatScore":
        vhWrap.vHarmonize.chordRepeatScore = value

# Associate Python functions with message address patterns, using default
# request the message address pattern before in argscheme
osc_method("/vectorHarmonizerControl", control_handler, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)
osc_method("/vectorHarmonizerNote", note_handler, argscheme=osm.OSCARG_ADDRESS + osm.OSCARG_DATAUNPACK)

def runloop():
    while True: osc_process()

# Start OSCServer
print("\nStarting VectorHarmonize OSCServer. Use ctrl-C to quit.")
st = threading.Thread( target = runloop )
st.start()

try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print("\nClosing OSCServer.")
    osc_terminate()
    print("Waiting for Server-thread to finish")
    st.join()
    print("Done")
