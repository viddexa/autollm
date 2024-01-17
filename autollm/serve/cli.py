import random
import time

import gradio as gr
from dotenv import load_dotenv
from llama_index import Document
from llama_index.prompts import ChatMessage

from autollm.auto.llm import AutoLiteLLM
from autollm.auto.query_engine import AutoQueryEngine

load_dotenv()


def create_preview(hf_api_key, make_db_private):
    # Placeholder for the logic to create the preview.
    preview_content = f"API Key: , DB Private: {make_db_private}"
    return preview_content


def submit_message(message):
    # Placeholder for the logic to process the message.
    return f"Message received: {message}"


def configure_app(config_file, emoji, name, description, instruction):
    # Here you would process the configuration file and inputs.
    # Placeholder function for the sake of example.
    return "Configuration updated (dummy response)."


llm = AutoLiteLLM.from_defaults()
# query_engine = AutoQueryEngine.from_defaults(documents=[Document.example()])


def predict(message, history):
    messages = [
        ChatMessage(role="system", content="You are an helpful AI assistant."),
        ChatMessage(role="user", content=message)
    ]
    chat_response = llm.chat(messages).message.content
    # chat_response = query_engine.query(message).response
    return chat_response


with gr.Blocks() as demo:
    gr.Markdown("### AutoLLM UI")  # Title for the app
    with gr.Row():
        with gr.Column():
            with gr.Tab("Create"):
                with gr.Tab("OpenAI"):
                    api_key_input = gr.Textbox(label="OPENAI_API_KEY", type="password")
                with gr.Tab("Palm"):
                    # Controls for 'Palm' tab
                    pass

                with gr.Column(variant="compact"):
                    file_upload = gr.File(label="Add knowledge from files", file_count="multiple")
                    webpage_input = gr.Textbox(label="Add knowledge from webpages")
                what_to_make_area = gr.Textbox(label="What would you like to make?")
                create_preview_button = gr.Button("Create Preview")

            with gr.Tab("Configure"):
                with gr.Column(variant="compact"):
                    detail_html = gr.HTML(
                        '<a href="https://github.com/safevideo/autollm/blob/main/examples/configs/config.example.yaml">click here for example config</a>'
                    )
                    config_file_upload = gr.File(label="Load .config file", file_count="single")
                    emoji_input = gr.Textbox(label="emoji:")
                    name_input = gr.Textbox(label="name:")
                    description_input = gr.TextArea(label="description:")
                    instruction_input = gr.TextArea(label="instruction:")
                    configure_button = gr.Button("Create Preview")
                    configure_button.click(
                        configure_app,
                        inputs=[
                            config_file_upload, emoji_input, name_input, description_input, instruction_input
                        ],
                        outputs=[])
            with gr.Tab("Export"):
                # Controls for 'Export' tab
                hf_api_key = gr.Textbox(label="Hf api key:", type="password")
                make_db_private = gr.Checkbox(label="Make db private")
                create_preview_button = gr.Button("Create Preview")
        with gr.Column():
            with gr.Row():
                download_api_button = gr.Button("Download API")
                deploy_button = gr.Button("Deploy to 🤗")

            gr.ChatInterface(predict)

    # Define interactions


def main():
    demo.launch()


if __name__ == "__main__":
    main()
