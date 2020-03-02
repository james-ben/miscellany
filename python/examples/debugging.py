# http://blog.devork.be/2009/07/how-to-bring-running-python-program.html
# This is an example of how to setup a program so that you 
#  can connect PDB to a running Python process by sending
#  a Unix signal to it 

import os
import signal
import sys
import time

# responds to signal
def handle_pdb(sig, frame):
    import pdb
    pdb.Pdb().set_trace(frame)

# stupid loop forever
def loop():
    while True:
        x = 'foo'
        time.sleep(0.2)

if __name__ == '__main__':
    # register signal handler
    signal.signal(signal.SIGUSR1, handle_pdb)
    # print the PID so we can send a signal to it
    print(os.getpid())
    loop()


# Then to enter the debugger, `kill -s SIGUSR1 [PID]`
