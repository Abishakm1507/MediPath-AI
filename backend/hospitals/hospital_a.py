from hospitals.hospital_utils import run_hospital_pipeline

async def run_hospital_a(symptoms: str):
    return await run_hospital_pipeline(symptoms, "Hospital A", "Cardiac Specialist")
