import asyncio
from hospitals.hospital_a import run_hospital_a
from hospitals.hospital_b import run_hospital_b
from hospitals.hospital_c import run_hospital_c

async def run_hospitals(symptoms: str):
    results = await asyncio.gather(
        run_hospital_a(symptoms),
        run_hospital_b(symptoms),
        run_hospital_c(symptoms)
    )
    return results
