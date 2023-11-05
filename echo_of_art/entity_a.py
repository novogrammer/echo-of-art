from cv2 import UMat

from runner import run
from dotenv import load_dotenv
import os

from filter_noop import filter_noop

if __name__ == '__main__':
  load_dotenv()
  MY_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
  YOUR_ADDRESS=os.getenv("EOA_ENTITY_B_ADDRESS","127.0.0.1")
  YOUR_PORT=int(os.getenv("EOA_ENTITY_B_PORT","5000"))

  print(f"MY_PORT: {MY_PORT}")
  print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
  print(f"YOUR_PORT: {YOUR_PORT}")

  run(filter_noop,MY_PORT,YOUR_ADDRESS,YOUR_PORT)