import gradio as gr
import requests
import base64
import json_repair
from pathlib import Path
import whisper

whisper_model = whisper.load_model("base")
running = False
transcription = ""

def run(frame, prompt, output):
  global running
  global transcription
  if running:
      return
  running = True
  frame = Path(frame)
  with open(frame, "rb") as f:
      encoded_string = base64.b64encode(f.read()).decode('utf-8')
  image_data = [{"data": encoded_string, "id": 42}]
  data = {"prompt": f"USER:[img-42] {prompt} and use this audio transcription: {transcription}.\nASSISTANT:", "n_predict": 4000, "image_data": image_data, "stream": True}
  try:
    response = requests.post(url="http://localhost:8080/completion", headers={"Content-Type": "application/json"}, json=data, stream=True)
  except Exception as e:
    running = False
    output += "■ Couldn't contact the llava server!\n\n"
    yield output
    return output
  output += "■ "
  for chunk in response.iter_content(chunk_size=128):
    content = chunk.decode().strip().split('\n\n')[0]
    try:
        content_split = content.split('data: ')
        if len(content_split) > 1:
            content_json = json_repair.loads(content_split[1])
            output += content_json["content"]
            yield output
    except Exception as e:
        print(e)
  running = False
  output += "\n\n"
  yield output
  return output

def transcribe(audio):
  global transcription
  if(audio):
    result = whisper_model.transcribe(audio)
    transcription = result['text']
  

css = """
  .upload-container > div:has(> .uploading) {
    display: none !important;
  }
  .hidden {
    display: none !important;
  }
"""

with gr.Blocks(css=css) as demo:
  with gr.Row():
    with gr.Column():
      webcam = gr.Image(sources=["webcam"], streaming=True, type="filepath", elem_classes="webcam")
      prompt = gr.Textbox(value="Describe a person in the image", label="Prompt")
      gr.Markdown("If you want to integrate audio transcript in the input for the AI. Press record")
      audio = gr.Microphone(streaming=True, type="filepath")
    with gr.Column():
      output = gr.Textbox(placeholder="Processing...", value="", label="Output")
    webcam.stream(run, inputs=[webcam, prompt, output], outputs=[output], show_progress=False)
    audio.stream(transcribe, inputs=[audio], show_progress=False)

if __name__ == "__main__":
  demo.launch(show_error=True)
