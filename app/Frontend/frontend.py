# import gradio as gr
# import requests
# import json


# # -----------------------------------
# # SEND REQUEST TO FASTAPI
# # -----------------------------------

# def analyze(audio, image):
    
#     print(audio)
#     print(type(audio))  


#     # Send files to FastAPI
#     files = {

#         "audio": open(audio, "rb"),

#         "image": open(image, "rb")
#     }

#     response = requests.post(

#         "http://127.0.0.1:8000/analyze",

#         files=files
#     )

#     print(response.status_code)

#     print(response.text)
#     result = response.json()

#     # Extract fields
#     patient_query = result["patient_query"]

#     diagnosis = json.dumps(
#         result["diagnosis"],
#         indent=4
#     )

#     audio_response = result["audio_response"]

#     return (
#         patient_query,
#         diagnosis,
#         audio_response
#     )


# # -----------------------------------
# # GRADIO UI
# # -----------------------------------

# with gr.Blocks() as demo:

#     gr.Markdown("# AI Doctor VoiceBot")

#     # Inputs
#     audio_input = gr.Audio(
#         sources=["microphone"],
#         type="filepath",
#         label="Speak Your Medical Query"
#     )

#     image_input = gr.Image(
#         type="filepath",
#         label="Upload Patient Image"
#     )

#     # Button
#     analyze_btn = gr.Button("Analyze")

#     # Outputs
#     transcript_output = gr.Textbox(
#         label="Patient Query"
#     )

#     diagnosis_output = gr.Textbox(
#         label="Structured Diagnosis",
#         lines=20
#     )

#     audio_response_output = gr.Audio(
#         label="Doctor Voice Response"
#     )

#     # Button Click
#     analyze_btn.click(

#         fn=analyze,

#         inputs=[
#             audio_input,
#             image_input
#         ],

#         outputs=[
#             transcript_output,
#             diagnosis_output,
#             audio_response_output
#         ]
#     )


# # Launch app
# demo.launch()