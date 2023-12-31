import socket
import os
from dotenv import load_dotenv

from image_transfer import receive_image

load_dotenv()


MY_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))
TO_FILE=bool(int(os.getenv("EOA_TO_FILE","1")))

print(f"MY_PORT: {MY_PORT}")
print(f"TO_FILE: {TO_FILE}")


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_receive:
  sock_for_receive.bind(("0.0.0.0", MY_PORT))

  sock_for_receive.listen(1)

  print("Waiting for connection...")

  file_count = 0

  while True:
    conn_for_receive, addr = sock_for_receive.accept()
    print(f"Connected by {addr}")

    while True:
      file_count += 1
      filename = f'received_image_{file_count}.jpg'

      data=receive_image(conn_for_receive)
      if data is None:
        print("Client disconnected.")
        conn_for_receive.close()
        break
      print("Received.")
      if TO_FILE:
        with open(filename, 'wb') as f:
          f.write(data)
      
    print("Waiting for next connection...")
