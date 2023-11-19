import pyaudio

audio = pyaudio.PyAudio()

for i in range(0, audio.get_device_count()):
    print(f"[{i}]['name']: {audio.get_device_info_by_index(i)['name']}")