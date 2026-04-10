from hospitals.hospital_utils import run_hospital_pipeline

async def run_hospital_c(symptoms: str):
    return await run_hospital_pipeline(symptoms, "Hospital C", "Emergency Hospital")
