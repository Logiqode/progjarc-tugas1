import socket
import logging
import os
import time
import datetime

logging.basicConfig(level=logging.INFO)

sending_time_str = "10:12:00"
sending_time = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(sending_time_str, "%H:%M:%S").time())

while datetime.datetime.now() < sending_time:
    time.sleep(0.5)

logging.info(f"File dikirim pada pukul {sending_time.strftime('%H:%M:%S')}")

def send_file(sock, file_path):
    try:
        # First send the file name
        file_name = os.path.basename(file_path)
        sock.sendall(file_name.encode('utf-8'))
        
        # Wait for server acknowledgment
        response = sock.recv(2)
        if response != b"OK":
            logging.error("Server rejected the file name")
            return False
            
        # Send file content
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                sock.sendall(data)
        return True
    except Exception as e:
        logging.error(f"Error sending file: {str(e)}")
        return False

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.16.16.101', 32444)
    logging.info(f"connecting to {server_address}")
    sock.connect(server_address)

    # Create file content
    file_content = "BITCOIN IS ALREADY ABOVE $100k! TIME TO BUY?"
    file_name = "bitcoin_alert_mesin2.txt"
    
    with open(file_name, 'w') as f:
        f.write(file_content)
    
    # Send the file
    logging.info(f"sending file: {file_name}")
    if send_file(sock, file_name):
        logging.info("File sent successfully")
    else:
        logging.error("Failed to send file")
        
except Exception as ee:
    logging.info(f"ERROR: {str(ee)}")
finally:
    sock.close()
    if os.path.exists(file_name):
        os.remove(file_name)
    logging.info("closing")
