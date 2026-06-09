
# This function takes the chat history and formats it into a single string that can be sent to the language model. 
def build_conversation(history):

    conversation = ""

    for msg in history:

        conversation += (
            f"{msg['role']}: {msg['content']}\n"
        )

    return conversation



def build_prompt(medical_response, conversation_history):

    prompt = f"""You are a helpful and precise medical assistant for doctors. 
    Your task is to help the doctor by providing relevant information based on the patient's medical report and the ongoing conversation.


    IMPORTANT:
    - Use the initial diagnosis as context.
    - Answer follow-up questions.
    - Do not diagnose life-threatening conditions with certainty.
    - Recommend consulting a doctor when appropriate.


    Here is the patient's medical report:
    {medical_response}

    Here is the conversation history between you and the doctor:
    {conversation_history}

    Based on the medical report and the conversation history, provide a helpful response to assist the doctor in diagnosing or treating the patient.
    """

    return prompt


def build_initial_text_prompt(patient_query: str) -> str:
    return f"""
You are an expert medical AI assistant.

A patient has described their symptoms or medical concern below.
Analyze it and respond ONLY with a valid JSON object. No explanation, no markdown, no preamble. Raw JSON only.

The JSON must strictly follow this schema:
{{
    "detected_issue": "Primary condition or symptom identified (string)",
    "description": "Detailed explanation of the condition and why you suspect it (string)",
    "severity": "One of exactly: mild | moderate | severe",
    "recommendations": ["actionable step 1", "actionable step 2", "..."],
    "should_consult_doctor": true or false,
    "confidence": a float between 0.0 and 1.0
}}

Rules:
- severity must be exactly one of: mild, moderate, severe
- confidence must reflect how certain you are based on the description alone
- recommendations must be a list of strings, not a single string
- should_consult_doctor must be a boolean
- Do NOT add any extra fields
- Do NOT wrap in markdown code blocks

Patient Query:
{patient_query}
"""