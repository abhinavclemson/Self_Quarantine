
import time

from pynput.keyboard import Listener
from threading import Thread

pressed=False

def on_press(key):
    print(f"Key pressed: {key}")
    global pressed
    pressed=True


with Listener(on_press=on_press) as ls:
    def time_out(period_sec: int):
        time.sleep(period_sec)  # Listen to keyboard for period_sec seconds
        ls.stop()

    Thread(target=time_out, args=(5,)).start()
    
    ls.join()
print(pressed)
