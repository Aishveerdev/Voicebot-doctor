from app.core.supabase_client import supabase
import logging
from app.models.schema import Medical_Response
logger = logging.getLogger(__name__)



# this is for new user report creation when they ask query for the first time  , that swhy user_id.
async def create_report(user_id: str, patient_query: str):
    try:
        logger.info(
            f"Creating medical report for user_id={user_id}"
        )

        response = (
            supabase.table("medical_report")
            .insert(
                {
                    "user_id": user_id,
                    "patient_query": patient_query,
                    "status": "processing",
                }
            )
            .execute()
        )

        # afterb the resposne is being cretaed , the first row will always be its very own report's id. so we can directly access it using response.data[0].get("id") and update the report later with diagnosis after vision model gives response.
        report_id = None
        if response.data:
            report_id = response.data[0].get("id")

        logger.info(
            f"Medical report created successfully. "
            f"report_id={report_id}, user_id={user_id}"
        )

        return report_id 
    # we dont need to retunr repsosne , but we need report id for update report fucntion to update the report with diagnosis after vision model gives response.

    except Exception as e:
        logger.exception(
            f"Failed to create medical report for user_id={user_id}: {e}"
        )
        raise


# this is for updating the report with diagnosis after vision model gives response , thats why report_id.
async def update_report(report_id: int, medical_response: Medical_Response):
    logger.info(f"medical_response type = {type(medical_response)}")
    try:
        logger.info(
            f"Updating medical report for report_id={report_id}"
        )

        response = (
            supabase.table("medical_report")
            .update(
                {
                    "medical_response": medical_response.model_dump(),
                    "status": "processed",
                }
            )
            .eq("id", report_id)
            .execute()
        )

        logger.info(
            f"Medical report updated successfully for report_id={report_id}"
        )

        return response

    except Exception as e:
        logger.exception(
            f"Failed to update medical report for report_id={report_id}: {e}"
        )
        raise


# get report history for a user using user_id from token and fetching all reports of that user from database.
async def get_report_history(user_id: str):
    # odro ayi user.id , edr recieve kiti as user_id , same thing.
    try:
        logger.info(f"Fetching report history for user_id={user_id}")

        response = (
            supabase.table("medical_report")
            .select("*")
            .eq("user_id", user_id)
            .execute()
        )

        logger.info(f"Retrieved report history for user_id={user_id}")

        return response.data
    except Exception as e:
        logger.exception(f"Failed to fetch report history for user_id={user_id}: {e}")
        raise 