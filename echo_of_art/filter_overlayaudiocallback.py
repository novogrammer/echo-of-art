
import os
from typing import Callable, Mapping
import cv2
from cv2 import UMat
import numpy as np
from dotenv import load_dotenv
import pyaudio
from my_timer import MyTimer
from queue import Empty,Full, Queue

from runner import run

SAMPLE_RATE = 44100             # サンプリングレート
# SAMPLE_RATE = 16000             # サンプリングレート
FRAME_SIZE = 2048               # フレームサイズ
INT16_MAX = 32767               # サンプリングデータ正規化用
SAMPLING_SIZE = 2048  # サンプリング配列サイズ

COLOR_AMPLIFIER = 20

class FilterOverlayAudioCallback:
  def __init__(self) -> None:
    self.isDestroyed=False
    load_dotenv()
    AUDIO_INDEX=int(os.getenv("EOA_AUDIO_INDEX","0"))
    print(f"AUDIO_INDEX: {AUDIO_INDEX}")


    # 周波数成分を表示用配列に変換する用の行列(spectram_array)作成
    #   FFT結果（周波数成分の配列)から、どの要素を合計するかをまとめた行列
    spectram_range = [int(22050 / 2 ** (i/10)) for i in range(20, -1,-1)]    # 21Hz～22,050Hzの間を分割
    # spectram_range = [int(8000 / 2 ** (i/10)) for i in range(20, -1,-1)]    # 8Hz～8,000Hzの間を分割
    self.spectram_range=spectram_range
    freq = np.abs(np.fft.fftfreq(SAMPLING_SIZE, d=(1/SAMPLE_RATE)))  # サンプル周波数を取得
    print(f"len(freq): {len(freq)}")
    # 一つ目
    self.spectram_array = (freq <= spectram_range[0]).reshape(1,-1)
    # それ以降
    for index in range(1, len(spectram_range)):
        tmp_freq = ((freq > spectram_range[index - 1]) & (freq <= spectram_range[index])).reshape(1,-1)
        self.spectram_array = np.append(self.spectram_array, tmp_freq, axis=0)


    self.audio = pyaudio.PyAudio()

    # サンプリング配列(sampling_data)の初期化
    self.sampling_data = np.zeros(SAMPLING_SIZE)

    self.frame_data_queue:Queue[np.ndarray[np.float64]] = Queue(10)

    stream_callback=self.make_stream_callback()
    self.stream = self.audio.open(format = pyaudio.paInt16,rate = SAMPLE_RATE,channels = 1,
                        input_device_index = AUDIO_INDEX,input = True,
                        frames_per_buffer=FRAME_SIZE,stream_callback=stream_callback)

  def __del__(self)->None:
    print("__del__")
    self.destroy()
  def destroy(self)->None:
    if not self.isDestroyed:
      self.isDestroyed=True
      self.stream.stop_stream()
      self.stream.close()
      self.audio.terminate()

  def make_stream_callback(self)->Callable[[bytes | None, int, Mapping[str, float], int], tuple[bytes | None, int]]:
    # 別スレッドのコールバックにキャプチャーさせたい
    frame_data_queue=self.frame_data_queue
    # 別スレッドで呼ばれる
    def stream_callback(in_data:bytes | None, frame_count:int, time_info:any, status:int):
      with MyTimer("overlayaudio frombuffer"):
        frame_data = np.frombuffer(in_data, dtype="int16") / INT16_MAX
      if frame_data_queue.full():
        # 古いものから捨てる
        print("drop frame_data")
        frame_data_queue.get()
      frame_data_queue.put(frame_data)
      # print(in_data)
      return (in_data, pyaudio.paContinue)
    return stream_callback

  def __call__(self, image_before:UMat) -> UMat:

    with MyTimer("overlayaudio np.concatenate"):
      while not self.frame_data_queue.empty():
        frame_data = self.frame_data_queue.get()
        # サンプリング配列に読み込んだデータを追加
        self.sampling_data = np.concatenate([self.sampling_data, frame_data])
      if self.sampling_data.shape[0] > SAMPLING_SIZE:
          # サンプリング配列サイズよりあふれた部分をカット
          self.sampling_data = self.sampling_data[self.sampling_data.shape[0] - SAMPLING_SIZE:]

    height,width,c = image_before.shape

    # 表示用の変数定義・初期化
    part_w = width / len(self.spectram_range)
    # img = np.full((height, width, 3), 0, dtype=np.uint8)

    with MyTimer("overlayaudio np.fft.fft"):
      # 高速フーリエ変換（周波数成分に変換）
      fft = np.abs(np.fft.fft(self.sampling_data))

    with MyTimer("overlayaudio np.dot"):
      # 表示用データ配列作成
      #   周波数成分の値を周波数を範囲毎に合計して、表示用データ配列(spectram_data)を作成
      spectram_data = np.dot(self.spectram_array, fft)

    # print(f"spectram_array.shape: {self.spectram_array.shape}")
    # print(f"fft.shape: {fft.shape}")

    with MyTimer("overlayaudio cv2.rectangle"):
      image_rectangles = np.zeros((height,width,c),np.uint8)
      # 出力処理
      # cv2.rectangle(img, (0,0), (width, height), (0,0,0), thickness=-1)   # 出力領域のクリア
      for index, value in enumerate(spectram_data):
        # 単色のグラフとして表示
        normalized_value = value / INT16_MAX
        x1=int(part_w * (index + 0))
        x2=int(part_w * (index + 1))
        
        additionalValue=min(normalized_value * 255 * COLOR_AMPLIFIER,255)
        additionalColor=(
          additionalValue,
          additionalValue,
          additionalValue,
        )
        # print(normalized_value)
        cv2.rectangle(image_rectangles,
                      (x1, int(height)),
                      (x2, int(0)),
                      additionalColor, thickness=-1)
    with MyTimer("overlayaudio merge"):
      # image_after = cv2.add(image_before,image_rectangles)
      image_after = cv2.bitwise_xor(image_before,image_rectangles)
      
    return image_after

if __name__ == '__main__':
  try:
    filter=FilterOverlayAudioCallback()
    MY_PORT=int(os.getenv("EOA_ENTITY_A_PORT","5000"))
    YOUR_ADDRESS=os.getenv("EOA_RECEIVER_ADDRESS","127.0.0.1")
    YOUR_PORT=int(os.getenv("EOA_RECEIVER_PORT","5000"))

    print(f"MY_PORT: {MY_PORT}")
    print(f"YOUR_ADDRESS: {YOUR_ADDRESS}")
    print(f"YOUR_PORT: {YOUR_PORT}")

    run(filter,MY_PORT,YOUR_ADDRESS,YOUR_PORT)
  finally:
    filter.destroy()
    # del filter
