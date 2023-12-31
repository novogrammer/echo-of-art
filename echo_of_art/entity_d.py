from cv2 import UMat

from runner import run
from dotenv import load_dotenv
import os

from filter_noop import FilterNoop
from filter_distance import FilterDistance

if __name__ == '__main__':
  filter=FilterDistance()
  # filter=FilterNoop()
  load_dotenv()
  MY_PORT=int(os.getenv("EOA_ENTITY_D_PORT","5000"))
  YOUR_ADDRESS=os.getenv("EOA_RECEIVER_ADDRESS","127.0.0.1")
  YOUR_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))

  print(f"MY_PORT: {MY_PORT}")
  print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
  print(f"YOUR_PORT: {YOUR_PORT}")

  run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT)