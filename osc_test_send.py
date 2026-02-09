#!/usr/bin/python
# -*- coding: latin-1 -*-
from osc4py3.as_eventloop import *
from osc4py3 import oscbuildparse
import time, threading

# Start the system.
osc_startup()

# Make client channels to send packets.
osc_udp_client("127.0.0.1", 8910, "aclientname")

# Build a simple message and send it.
msg = oscbuildparse.OSCMessage("/vectorHarmonizerControl", "i", [48])
osc_send(msg, "aclientname")
msg = oscbuildparse.OSCMessage("/vectorHarmonizerControl", ",iii", [60,62,1])
osc_send(msg, "aclientname")
msg = oscbuildparse.OSCMessage("/vectorHarmonizerNote", ",iii", [61,62,1])
osc_send(msg, "aclientname")
msg = oscbuildparse.OSCMessage("/vectorHarmonizerNote", ",iii", [62,62,1])
osc_send(msg, "aclientname")
msg = oscbuildparse.OSCMessage("/vectorHarmonizerControl", "i", [49])
osc_send(msg, "aclientname")

print("sent messages")

def runloop():
    while True: osc_process()

# Start OSCServer
print("\nStarting OSC sender Use ctrl-C to quit.")
st = threading.Thread( target = runloop )
st.start()

try :
    while 1 :
        time.sleep(5)
        print("running")

except KeyboardInterrupt :
    print("\nClosing OSCServer.")
    osc_terminate()
    print("Waiting for Server-thread to finish")
    st.join()
    print("Done")
