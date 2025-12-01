import gradio as gr
import requests
import json
from datetime import datetime

# Ganti dengan URL webhook n8n kamu
N8N_WEBHOOK = "https://your-n8n-url.onrender.com/webhook/agent"

def send_to_backend(user_id, text, file=None, lang_hint="auto"):
    payload = {
        "user_id": user_id,
        "text": text,
        "lang_hint": lang_hint,
        "timestamp": datetime.utcnow().isoformat()
    }

    files = None
    if file:
        files = {"file": (file.name, file.read())}

    try:
        if files:
            response = requests.post(N8N_WEBHOOK, data=payload, files=files, timeout=60)
        else:
            response = requests.post(N8N_WEBHOOK, json=payload, timeout=60)
        
        return json.dumps(response.json(), indent=2, ensure_ascii=False)

    except Exception as e:
        return f"Error: {str(e)}"


with gr.Blocks(title="Pujo Multilingual AI Orchestrator") as demo:
    
    gr.Markdown("## 🇯🇵🇺🇸 Multilingual AI Orchestrator — JP / EN")

    with gr.Row():
        user_id = gr.Textbox(label="User ID", value="user-1")
        lang_hint = gr.Radio(["auto", "JP", "EN"], value="auto", label="Force Language")

    text_input = gr.Textbox(label="Text Input", placeholder="Write message here...")
    file_input = gr.File(label="Upload CSV (optional)", file_types=[".csv"])
    output_box = gr.Textbox(label="Response", lines=10)
    
    btn = gr.Button("Send")

    btn.click(
        send_to_backend,
        inputs=[user_id, text_input, file_input, lang_hint],
        outputs=[output_box]
    )

demo.launch()
