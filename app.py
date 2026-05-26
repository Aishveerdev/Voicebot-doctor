import gradio as gr
import asyncio    
from dotenv import load_dotenv
from audio_recorder import record_audio
from speech_to_text import transcribe_audio
from text_to_speech import speak_text
from llm import ask_vision_model
from text_to_speech import speak_text

load_dotenv()





async def main(audio, image):


    patient_query = transcribe_audio(audio)
    #4. Get medical response
    medical_response = ask_vision_model(image, patient_query)
    
    #5. Speak out response
    response_text = medical_response.spoken_response
    speak_task = asyncio.create_task(speak_text(response_text))

    return (
    patient_query,
    medical_response.model_dump_json(indent=4)
    )


with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown(
        """
        # 🩺 AI Medical Vision Assistant

        Upload image + speak symptoms.
        """
    )

    with gr.Row():

        image_input = gr.Image(
            type="filepath",
            label="Upload Medical Image"
        )

        audio_input = gr.Audio(
            sources=["microphone"],
            type="filepath",
            label="Speak Symptoms"
        )


    analyze_btn = gr.Button("Analyze")


    transcript_output = gr.Textbox(
        label="Patient Query"
    )


    diagnosis_output = gr.Textbox(
        label="Structured Diagnosis",
        lines=20
    )


    analyze_btn.click(
        fn=main,
        inputs=[
            audio_input,
            image_input
        ],
        outputs=[
            transcript_output,
            diagnosis_output
        ]
    )


# =========================================
# LAUNCH
# =========================================

demo.launch()