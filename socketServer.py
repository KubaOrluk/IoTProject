import numpy as np
import encodings
from socket import *
import socket
import qwiic_bme280
import time
import sys
from datetime import datetime
import json

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode


mySensor = qwiic_bme280.QwiicBme280()

mySensor.begin()

HOST = '192.168.1.106'  # Standard loopback interface address (localhost)
PORT = 63332           # Port to listen on (non-privileged ports are > 1023)

key = b"\x81:\x8eGp\x1eL'1\xf8\xf71\xef\xeb\x911"



def take_data_from_sensor():
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        data = {
           "date": current_time,
           "temperature": mySensor.temperature_celsius
            }
        result = json.dumps(data)
        return result


def encrypt_data(data):
    data = bytes(data, 'utf-8')

    cipher = AES.new(key, AES.MODE_CTR)
    ct_bytes = cipher.encrypt(data)
    nonce = b64encode(cipher.nonce).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')

    result = json.dumps({'nonce':nonce, 'ciphertext':ct})
    return result


def my_server():
    print("Server is now running ...")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print(f'{addr} is connected.')
                while True:

                    data = conn.recv(1024).decode('utf-8')

                    if str(data) == "Data":

                        print("Sending data ...")

                        try:
                            my_data = take_data_from_sensor()
                        except(Exception):
                            print("Something went wrong with obtaining data from sensor.")

                        encrypted_data = encrypt_data(my_data)

                        encoded_data = encrypted_data.encode('utf-8')

                        conn.sendall(encoded_data)

                    if not data:
                        break
                    else:
                        pass
                


if __name__ == '__main__':
    my_server()
