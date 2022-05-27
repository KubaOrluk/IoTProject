try:
    import socket
    import threading
    import time
    import json
    import os
    import mysql.connector as database

    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util.Padding import pad, unpad
    from base64 import b64decode, b64encode

except:
    print('!!!!#### Critical ERROR: Library not found ####!!!!')



HOST = '192.168.0.14'  # The server's hostname or IP address
PORT = 63332       # The port used by the server

key = b"\x81:\x8eGp\x1eL'1\xf8\xf71\xef\xeb\x911"


def connect_to_database():
    username = os.environ.get("pi")
    password = os.environ.get("raspberry")

    connection = database.connect(
        user="glowlicensefree",
        password="themeduckpioneer",
        host='127.0.0.1',
        database="temperatures")
    return connection

def add_data(temperature, data, connection):
    cursor = connection.cursor()
    try:
        statement = "INSERT INTO project (temperature, data) Values (%s, %s)"
        dane = (temperature, data)
        cursor.execute(statement, dane)
        connection.commit()
        print("Data inserted")
    except database.Error as e:
        print(f"Something went wrong: {e}")


def decrypt_data(data):
    try:
        b64 = json.loads(data)
        nonce = b64decode(b64['nonce'])
        ct = b64decode(b64['ciphertext'])

        cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
        pt = cipher.decrypt(ct)

        return pt
    except (ValueError, KeyError):
        print("Something went wrong with decryption.")


def process_data_from_server(input_data):        # Define function to split Incoming Data
    data = json.loads(decrypt_data(input_data))
    return data


def my_client():
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:        # define socket TCP
            s.connect((HOST, PORT))

            my_inp = 'Data'
            # encode the message
            my_inp = my_inp.encode('utf-8')

            # send request to server
            s.sendall(my_inp)

            # Get the Data from Server and process the Data
            data = s.recv(1024).decode('utf-8')

            recdata = process_data_from_server(data)

            print("Date: {}".format(recdata['date']))
            print("Temperature: {}".format(recdata['temperature']))

            s.close()
            connection = connect_to_database()
            add_data(round(recdata['temperature'],1), recdata['date'], connection)
            connection.close()
            time.sleep(900)


if __name__ == "__main__":
    my_client()
