import os 
import socket
from Crypto.Cipher import AES

key = b"ElectroMagnetism"
nonce = b"ElectroMagnetOnc"

cipher = AES.new(key, AES.MODE_EAX, nonce) 

client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("localhost" , 8080 ))


file_size = os.path.getsize("C:\clg\python_project\zile.txt")

with open("C:\clg\python_project\zile.txt" , "rb") as f:
    data = f.read()

encrypted = cipher.encrypt(data)

client.send("new.txt".encode())
client.send(str(file_size).encode())
client.sendall(encrypted)
client.send(b"<END>")

client.close()



