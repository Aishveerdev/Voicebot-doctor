import logging
from app.services.llm import ask_language_model_strucutred,ask_language_model_formal
from app.services.reports import get_report_by_id
from app.services.redis_memory import get_chat_context
from app.services.redis_func import add_message
from app.services.supabase_db import save_message , get_chat_session ,update_chat_session 
from app.services.reports import create_report , update_report
from app.models.prompt import build_conversation, build_prompt , build_initial_text_prompt
from app.models.schema import API_Response , ChatResponse



logger = logging.getLogger(__name__)





async def process_text_query(user , patient_query , session_id=None):
    logger.info(f"Current user id: {user.id}")
    try:
        logger.info("query received for text processing, starting processing")

        # Get session
        session = await get_chat_session(session_id)  # we will provide medical diagnosis from
        report = None

        if session.get("report_id"): # This means if any report ius iattached to session then ,
           report = await get_report_by_id(session["report_id"]) # get that report .
        

        # this checks if report is validf or not.
        new_text_only_session = (
            not session.get("report_id") or
            not report or
            report[0].get("status") != "processed" or
            not report[0].get("medical_response")
        )

        if new_text_only_session:
            logger.info("No valid report attached to session %s — creating/updating report", session_id)

            # If there's no report id, create one and attach to session
            if not session.get("report_id"):
                logger.info(f"creating new report for user_id={user.id} with patient_query={patient_query}")
                report_id = await create_report(user.id, patient_query)

                logger.info(f"Updating chat session {session_id} with report_id={report_id}")
                await update_chat_session(session_id, report_id)
                logger.info(f"Chat session {session_id} updated ✅ with report_id={report_id}")
            else:
                report_id = session["report_id"]

            # Build formal prompt to produce exact Medical_Response schema
            prompt = build_initial_text_prompt(patient_query)
            try:
                logger.info("Asking language model ( structured medical response)")
                ai_medical_response = await ask_language_model_strucutred (prompt)
                logger.info("Structured medical response generated ✅")
            except Exception:
                logger.exception("Structured LLM call failed for session %s", session_id)
                raise

            # Update report with structured medical response
            await update_report(report_id, medical_response=ai_medical_response)
            logger.info("Report updated for report_id=%s", report_id)

            # Save user message and assistant structured response
            await save_message(session_id, role="user", content=patient_query) # in DB
            await add_message(session_id, role="user", content=patient_query) # in Redis

           # Save assistant message 
            await save_message(session_id, role="assistant", content=ai_medical_response.description)
            await add_message(session_id, role="assistant", content=ai_medical_response.description)

            logger.info("/chat/message completed for session %s", session_id)
            return API_Response(
                patient_query=patient_query,
                diagnosis=ai_medical_response,
                session_id=session_id,
                report_id=report_id,
            )




        else:
            # Existing valid report -> follow-up conversation
            report = await get_report_by_id(session["report_id"])
            report_id = session["report_id"]
            logger.info("Fetched report for report_id=%s -> %s", report_id, "found" if report else "not found")

            # Get chat history and include current patient query as the latest user message
            history = await get_chat_context(session_id) or []
            logger.info("Fetched chat history for session %s (entries=%d)", session_id, len(history))

            # Append the latest user query to history for context
            history.append({"role": "user", "content": patient_query})
            conversation_history = build_conversation(history)

            # Build prompt for follow-up (do NOT return full structured medical_response again)
            prompt = build_prompt(medical_response=report[0]["medical_response"], conversation_history=conversation_history)
            logger.debug("Built prompt for follow-up LLM (prompt_len=%d)", len(prompt) if prompt else 0)

            try:
                logger.info("Asking language model (follow-up, non-full-structured reply)")
                ai_response = await ask_language_model_formal(prompt)
                logger.info("Follow-up response generated ✅")
            except Exception:
                logger.exception("Follow-up LLM call failed for session %s", session_id)
                raise

            # Save user message and assistant follow-up
            await save_message(session_id, role="user", content=patient_query)
            await add_message(session_id, role="user", content=patient_query)

            assistant_content = ai_response if isinstance(ai_response, str) else str(ai_response)
            await save_message(session_id, role="assistant", content=assistant_content)
            await add_message(session_id, role="assistant", content=assistant_content)

           
      
        if new_text_only_session :
            return API_Response(
                patient_query=patient_query,
                diagnosis=ai_response,
                session_id=session_id,
                report_id=report_id,
            )
        else:
            return ChatResponse(
        patient_query=patient_query,
        response=ai_response,           # plain string
        session_id=session_id,
        report_id=report_id)




    except Exception as e:
        logger.exception(e)
        raise
