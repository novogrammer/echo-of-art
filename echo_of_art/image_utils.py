import cv2
from cv2 import UMat

def crop_and_resize(frame:UMat,width:int,height:int)->UMat:
  aspect=float(height)/float(width)
  [original_height,original_width]=frame.shape[0:2]
  original_aspect=float(original_height)/float(original_width)
  if aspect < original_aspect:
    # 高さが不要
    temporary_height=int(original_width * aspect)
    y=int((original_height - temporary_height)/2)
    cropped_frame=frame[y:temporary_height,0:original_width]
  else:
    # 幅が不要
    temporary_width=int(original_height / aspect)
    x=int((original_width - temporary_width)/2)
    cropped_frame=frame[0:original_height,x:temporary_width]
  resized_frame=cv2.resize(cropped_frame, (width,height),interpolation=cv2.INTER_NEAREST)
  return resized_frame

