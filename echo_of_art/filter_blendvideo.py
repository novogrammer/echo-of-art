
import os
import cv2
from cv2 import UMat
from dotenv import load_dotenv
from image_utils import crop_and_resize
from my_timer import MyTimer

from runner import run

class FilterBlendVideo:
  def __init__(self) -> None:

    load_dotenv()
    VIDEO_INDEX=int(os.getenv("EOA_VIDEO_INDEX","0"))
    print(f"VIDEO_INDEX: {VIDEO_INDEX}")

    self.capture=cv2.VideoCapture(VIDEO_INDEX)
    self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    # self.capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('Y','U','Y','V'))
    self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    self.capture.set(cv2.CAP_PROP_FPS, 15)

  def __call__(self, image_before:UMat) -> UMat:
    if not self.capture.isOpened():
      print("not capture.isOpened()")
      return image_before

    result_read,frame=self.capture.read()
    if not result_read:
      print("not result_read")
      return image_before
    height,width,c = image_before.shape
    with MyTimer("resize"):
      resized_frame=crop_and_resize(frame,width,height)
    resized_frame=cv2.flip(resized_frame,1)
    image_after=image_before.copy()
    image_after[:,:,0]=resized_frame[:,:,0]
    # image_after=cv2.addWeighted(image_before,0.5,resized_frame,0.5,0.0)
    return image_after

if __name__ == '__main__':
  filter=FilterBlendVideo()
  load_dotenv()
  MY_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
  YOUR_ADDRESS=os.getenv("EOA_RECEIVER_ADDRESS","127.0.0.1")
  YOUR_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))

  print(f"MY_PORT: {MY_PORT}")
  print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
  print(f"YOUR_PORT: {YOUR_PORT}")

  run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT)
