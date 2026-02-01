import gradio as gr
from prompt import REFEREE_SYSTEM_PROMPT
from utils import analyzing_var_footage

with gr.Blocks() as demo: 
    gr.Markdown("# Analyze VAR Footage with LLMs")

    with gr.Row():
        with gr.Column():
            video_input = gr.Video(label="Upload Video")
            submit_btn = gr.Button("Analyze Video",variant="primary")
            
        with gr.Column():
            output_text = gr.Textbox(
                label="Claude's Response",
                lines=15,
                interactive=False
            )

        submit_btn.click(fn=analyzing_var_footage,
                             inputs=video_input,
                             outputs=output_text)

if __name__ == "__main__":
    demo.launch()