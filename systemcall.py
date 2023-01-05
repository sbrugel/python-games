import os, threading

class SystemCall(threading.Thread):
    """
    Runs the shell command specified in the 'command' parameter in a separate thread.
    """
    def __init__(self, command):
        threading.Thread.__init__(self)
        self.command = command
 
    def run(self):
        os.system(self.command)