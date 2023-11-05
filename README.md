# アートのエコー
HOMEWORKS 2023で展示する作品


## PyAudioの準備
PyAudioの準備

### Macの場合

```bash
brew install portaudio
```

### Ubuntuの場合

```bash
sudo apt-get install portaudio19-dev
```

## 環境構築

poetryをインストールしておく

```bash
poetry install
```
## 環境変数

`pyproject.toml`と同じ階層に`.env`を置く

```
EOA_ENTITY_A_ADDRESS="127.0.0.1"
# EOA_ENTITY_A_ADDRESS="MacBook-Pro-2.local"
# EOA_ENTITY_A_ADDRESS="raspi400.local"
EOA_ENTITY_A_PORT="5001"

EOA_ENTITY_B_ADDRESS="127.0.0.1"
# EOA_ENTITY_B_ADDRESS="raspi4-01.local"
EOA_ENTITY_B_PORT="5002"

EOA_ENTITY_C_ADDRESS="127.0.0.1"
# EOA_ENTITY_C_ADDRESS="raspi4-02.local"
EOA_ENTITY_C_PORT="5003"

EOA_ENTITY_D_ADDRESS="127.0.0.1"
# EOA_ENTITY_D_ADDRESS="raspi400.local"
EOA_ENTITY_D_PORT="5004"

EOA_RECEIVER_ADDRESS="127.0.0.1"
# EOA_RECEIVER_ADDRESS="raspi400.local"
EOA_RECEIVER_PORT="5005"


# sender.pyでファイルから読み込むか？
EOA_FROM_FILE="0"

# sender.pyやentity_*.pyでつかうVIDEOのINDEX
EOA_VIDEO_INDEX="0"
# entity_*.pyでつかうAUDIOのINDEX
# Macで試す場合
EOA_AUDIO_INDEX="0"
# raspi4はHDMIが0番目なので1番目を使う
# EOA_AUDIO_INDEX="1"
# entity_*.pyでつかうARDUINO_HCSR04
# Macで試す場合
EOA_ARDUINO_HCSR04_DEVICE="/dev/cu.usbmodem2101"
# raspi4で検出されるデバイス名
# EOA_ARDUINO_HCSR04_DEVICE="/dev/ttyACM0"
# 画像幅
EOA_IMAGE_WIDTH="320"
# EOA_IMAGE_WIDTH="480"
# EOA_IMAGE_WIDTH="1280"
# 画像高さ
EOA_IMAGE_HEIGHT="180"
# EOA_IMAGE_HEIGHT="270"
# EOA_IMAGE_HEIGHT="720"
# sender.pyのFPS
EOA_FPS="15"

# receiver.pyでファイルへ書き込むか？
EOA_TO_FILE="0"

```

