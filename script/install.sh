#!/bin/bash

set -ex

LOGFILE="sichiribe_install_$(date '+%Y-%m-%d_%H-%M-%S').log"
exec > >(tee -i "$LOGFILE") 2>&1

ARCH=$(uname -m)
cd ~

# tensorflow-src ディレクトリが存在しない場合にクローン
if [ ! -d "tensorflow-src" ]; then
    git clone https://github.com/tensorflow/tensorflow tensorflow-src
fi
cd tensorflow-src

# ビルド環境を作成
python -m venv env 
source ./env/bin/activate
pip install numpy wheel pybind11

# MacOS用にビルドを実行
CUSTOM_BAZEL_FLAGS=--macos_cpus=$ARCH tensorflow/lite/tools/pip_package/build_pip_package_with_bazel.sh

# ビルド済みwhlパッケージを確認
WHL_FILE=$(ls ~/tensorflow-src/tensorflow/lite/tools/pip_package/gen/tflite_pip/python3/dist/*.whl)

# ビルド環境をから抜ける
deactivate

# アプリケーションのビルド環境を作成
cd ~
rm -rf sichiribe-src
git clone https://github.com/EbinaKai/Sichiribe.git sichiribe-src
cd sichiribe-src
git checkout feature/app/macos
python -m venv env
source ./env/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install $WHL_FILE
pip install nuitka zstandard orderedset imageio

# モデルファイルをダウンロードするURL
MODEL_URL="https://github.com/EbinaKai/Sichiribe/releases/download/v0.1.2/model_100x100.tflite"
MODEL_DIR="./model"
MODEL_FILE="$MODEL_DIR/model_100x100.tflite"

# モデルファイルをダウンロード
mkdir -p "$MODEL_DIR"
curl -L -o "$MODEL_FILE" "$MODEL_URL"

# ビルド
BILD_SCRIPT="./script/build.sh"
if [ -f "$BILD_SCRIPT" ]; then
    bash "$BILD_SCRIPT"
else
    echo "ビルドスクリプトが見つかりません。"
fi
