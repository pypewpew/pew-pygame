import os
import subprocess
import sys
import time

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

WATCHED_FILE = sys.argv[1] if len(sys.argv)>1 else "code.py"
REFRESH_CYCLE = 0.2

previous = 0
process = None

if not os.path.isfile(WATCHED_FILE):
    print(f"Error: {WATCHED_FILE} not found!")
    sys.exit(0)

try:
    while True:
        modified = os.stat(WATCHED_FILE).st_mtime
        if modified > previous:
            now = time.strftime("%H:%M:%S", time.localtime())
            print(f"{now} - {WATCHED_FILE} was modified - reloading!")
            previous = modified
            if process:
                process.kill()

            process = subprocess.Popen(["python", WATCHED_FILE], shell=False)
        
        time.sleep(REFRESH_CYCLE)

except KeyboardInterrupt:
    if process:
        process.kill()
    print("\nCTRL-C detected, autoloader stopped.")