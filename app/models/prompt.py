
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