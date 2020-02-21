import os
import subprocess
import sys
import webview
import atexit
import signal

# # Create subprocess
# PID = os.fork()
#
# # Exit routine that kills the subprocess nicely
# def kill_child_process(pid):
#     os.kill(pid, signal.SIGSTOP)
#
# # Add the subprocess killer to be run when the app is killed
# atexit.register(kill_child_process, pid=PID)
#
# # The new process will be the server and the parnet will be the frontend
# if (PID == 0):
#     print (sys.executable)
#     os.execv(sys.executable, ['python3', 'server/main.py'])
# else:
#     #webview.create_window('Window', 'http://localhost:5000/', frameless=True, )
#     #webview.start()
#     pass

subprocess.run(['python3', 'server/main.py'])
