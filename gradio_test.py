import pandas as pd

URL = "https://docs.google.com/spreadsheets/d/12XgTyn5iJyKhvirhi-xyhLBgx_uXJz6ELBwpkW-G4UM/edit#gid=0"
csv_url = URL.replace('/edit#gid=', '/export?format=csv&gid=')

def get_data():
    return pd.read_csv(csv_url)

import gradio as gr

with gr.Blocks() as demo:
    gr.Markdown("# 📈 Real-Time Line Plot")
    with gr.Row():
        with gr.Column():
            gr.DataFrame(get_data, every=5)
        with gr.Column():
            gr.LinePlot(get_data, every=5, x="Pt Interarrival Time (lambda)", y="Median_Q_Rec_time", y_title="Median queue time for receptionist (min)", overlay_point=True, width=500, height=500)

demo.queue().launch()  # Run the demo with queuing enabled
