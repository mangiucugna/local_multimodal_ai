# Install

### 1. Clone this repository

```
git clone https://github.com/mangiucugna/local_multimodal_ai
```

### 2. Clone llama.cpp

```
git clone https://github.com/ggerganov/llama.cpp
```

### 3. Download AI Model

Download the following bakllava model files to the `llama.cpp/models` folder

- https://huggingface.co/mys/ggml_bakllava-1/resolve/main/ggml-model-q4_k.gguf
- https://huggingface.co/mys/ggml_bakllava-1/resolve/main/mmproj-model-f16.gguf

### 4. Build llama.cpp


```
cd llama.cpp
mkdir build
cd build
cmake ..
cmake --build . --config Release
```

### 5. Install requirements

Create a venv and install requirements

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6. Install prerequisites

Install FFMPEG: https://ffmpeg.org/download.html

For Mac (using brew)

```
brew install ffmpeg
```

### 7. Launch the llama.cpp server

First start the llama.cpp server:

#### Windows

```
cd llama.cpp\build\bin
Release\server.exe -m ..\..\ggml-model-q4_k.gguf --mmproj ..\..\mmproj-model-f16.gguf -ngl 1
```

#### Mac & Linux

```
cd llama.cpp/build/bin
./server -m ../../ggml-model-q4_k.gguf --mmproj ../../mmproj-model-f16.gguf -ngl 1
```

#### 8. Launch the web UI
Open another terminal window

```
source .venv/bin/activate
python app.py
```


# Credits

1. Forked from https://github.com/cocktailpeanut/mirror/
2. [Llama.cpp](https://github.com/ggerganov/llama.cpp)
3. [Bakllava](https://huggingface.co/SkunkworksAI/BakLLaVA-1)
4. Built with [gradio](https://www.gradio.app/).

