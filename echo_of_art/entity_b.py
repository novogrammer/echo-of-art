from cv2 import UMat

from runner import run
from dotenv import load_dotenv
import os

from filter_noop import FilterNoop
from filter_blendvideo import FilterBlendVideo

if __name__ == '__main__':
  try:
    filter=FilterBlendVideo()
    # filter=FilterNoop()
    load_dotenv()
    MY_PORT=int(os.getenv("EOA_ENTITY_B_PORT","5000"))
    YOUR_ADDRESS=os.getenv("EOA_ENTITY_C_ADDRESS","127.0.0.1")
    YOUR_PORT=int(os.getenv("EOA_ENTITY_C_PORT","5000"))

    print(f"MY_PORT: {MY_PORT}")
    print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
    print(f"YOUR_PORT: {YOUR_PORT}")

    run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT)
  finally:
    filter.destroy()