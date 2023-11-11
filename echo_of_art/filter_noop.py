
import cv2
from cv2 import UMat

from runner import run
from dotenv import load_dotenv
import os

class FilterNoop:
  def __init__(self) -> None:
    pass
  def __call__(self, image_before:UMat) -> UMat:
    image_after=image_before.copy()
    return image_after


if __name__ == '__main__':
  filter=FilterNoop()
  load_dotenv()
  MY_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
  YOUR_ADDRESS=os.getenv("EOA_RECEIVER_ADDRESS","127.0.0.1")
  YOUR_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))

  print(f"MY_PORT: {MY_PORT}")
  print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
  print(f"YOUR_PORT: {YOUR_PORT}")
  run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT)
