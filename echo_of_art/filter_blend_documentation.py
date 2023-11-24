
import cv2
from cv2 import UMat
from filter_noop import FilterNoop

from runner import run
from dotenv import load_dotenv
import os
import numpy as np

class FilterBlendDocumentation:
  def __init__(self) -> None:
    with open('documentation/documentation.png', 'rb') as f:
      data = f.read()
    image_buf=np.frombuffer(data,dtype=np.uint8)
    self.image_documentation=cv2.imdecode(image_buf,cv2.IMREAD_COLOR)
    pass
  def __call__(self, image_before:UMat) -> UMat:
    image_after=self.image_documentation.copy()
    [height,width]=image_before.shape[0:2]
    image_after[0:height,0:width]=image_before
    return image_after


if __name__ == '__main__':
  filter=FilterNoop()
  filter_documentation=FilterBlendDocumentation()
  load_dotenv()
  MY_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
  YOUR_ADDRESS=os.getenv("EOA_RECEIVER_ADDRESS","127.0.0.1")
  YOUR_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))

  print(f"MY_PORT: {MY_PORT}")
  print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
  print(f"YOUR_PORT: {YOUR_PORT}")
  run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT,filter_for_display=filter_documentation)
