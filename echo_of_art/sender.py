import socket
import os
import time
import constants
from my_timer import MyTimer

from dotenv import load_dotenv

from image_transfer import send_image
import cv2
from image_utils import crop_and_resize

load_dotenv()

YOUR_ADDRESS=os.getenv("EOA_ENTITY_A_ADDRESS","127.0.0.1")
YOUR_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
FROM_FILE=bool(int(os.getenv("EOA_FROM_FILE","1")))
VIDEO_INDEX=int(os.getenv("EOA_VIDEO_INDEX","0"))
IMAGE_WIDTH=int(os.getenv("EOA_IMAGE_WIDTH","480"))
IMAGE_HEIGHT=int(os.getenv("EOA_IMAGE_HEIGHT","270"))
FPS=int(os.getenv("EOA_FPS","30"))
SPF=1/FPS

print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
print(f"YOUR_PORT: {YOUR_PORT}")
print(f"FROM_FILE: {FROM_FILE}")
print(f"VIDEO_INDEX: {VIDEO_INDEX}")
print(f"IMAGE_WIDTH: {IMAGE_WIDTH}")
print(f"FPS: {FPS}")

if FROM_FILE:
  with open('sending_image.jpg', 'rb') as f:
    data = f.read()
else:
  capture=cv2.VideoCapture(VIDEO_INDEX)
  capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
  # capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
  capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
  capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
  capture.set(cv2.CAP_PROP_FPS, 15)
while True:
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_for_send:
      sock_for_send.connect((YOUR_ADDRESS, YOUR_PORT))

      if FROM_FILE:
        send_image(sock_for_send,data)
        print("Sent.")
      else:
        previous_time=time.perf_counter()
        # frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        # frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        while capture.isOpened():
          before_sleep_time=time.perf_counter()
          time.sleep(max(0,SPF - (before_sleep_time - previous_time)))
          previous_time=time.perf_counter()
          result_read,frame=capture.read()
          if not result_read:
            print("not result_read")
            continue
          # print(f"w:{frame.shape[1]} h:{frame.shape[0]}")
          with MyTimer("resize"):
            resized_frame=crop_and_resize(frame,IMAGE_WIDTH,IMAGE_HEIGHT)
            resized_frame=cv2.flip(resized_frame,1)
          result_encode,encoded=cv2.imencode(".jpg", resized_frame, (cv2.IMWRITE_JPEG_QUALITY, constants.JPEG_QUALITY))
          if not result_encode:
            print("not result_encode")
            continue
          data=encoded.tobytes()
          send_image(sock_for_send,data)
          # print("Sent.")
        break
  except socket.error as e:
    print(e)
    print("retry connect")
    time.sleep(1)

