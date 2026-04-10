from hospitals.hospital_utils import run_hospital_pipeline

async def run_hospital_b(symptoms: str):
    return await run_hospital_pipeline(symptoms, "Hospital B", "General Hospital")
