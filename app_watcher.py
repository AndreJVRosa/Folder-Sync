import os
import sys
import subprocess
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

class RestartHandler(PatternMatchingEventHandler):
    def __init__(self, patterns=None):
        super().__init__(patterns=patterns)
        self.process = None

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith("gui.py"):
            print(f'Restarting due to change in: {event.src_path}')
            self.restart_script()

    def restart_script(self):
        self.process.terminate()
        self.process.wait()
        self.start_script()

    def start_script(self):
        python_executable = sys.executable
        script_directory = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_directory, "gui.py")
        self.process = subprocess.Popen([python_executable, script_path])

def monitor_gui():
    patterns = ["gui.py"]  # Patterns to watch for changes
    event_handler = RestartHandler(patterns=patterns)

    # Start the script initially
    event_handler.start_script()

    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)

    try:
        print("Watching for changes...")
        observer.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    monitor_gui()
