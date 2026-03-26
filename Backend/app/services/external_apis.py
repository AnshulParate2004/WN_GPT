"""
External APIs — Integration layer for Fitbit/ABDM/wearable data.
In production these will make real HTTP calls; stub implementations are used for demo.
"""
from __future__ import annotations
import httpx
from app.db import repository as repo


async def fetch_abdm_records(abha_id: str) -> list[dict]:
    """
    Fetch patient health records from ABDM/NHA Health Locker.
    Stub: returns patient data from Supabase as a stand-in.
    Production: POST to https://healthid.abdm.gov.in/api/v1/... with ABDM auth tokens.
    """
    patient = repo.get_patient_by_abha(abha_id)
    if not patient:
        return []
    return [
        {
            "source": "ABDM",
            "record_type": "patient_profile",
            "data": patient,
        }
    ]


async def fetch_wearable_data(patient_id: str, device: str = "fitbit") -> list[dict]:
    """
    Pull wearable data (steps, heart rate, sleep) from Fitbit / Apple Health / Google Fit.
    Stub: returns from Supabase wearable_data table.
    Production: Use OAuth2 + device-specific APIs.
    """
    return repo.get_wearable_data(patient_id)


async def send_sms_reminder(phone: str, message: str) -> bool:
    """
    Send SMS reminder via Twilio / MSG91.
    Stub: just returns True.
    Production: POST to Twilio Messages API.
    """
    # In production: use Twilio client or MSG91 API
    print(f"[SMS STUB] To: {phone} | Message: {message}")
    return True


async def send_push_notification(patient_id: str, title: str, body: str) -> bool:
    """
    Send push notification via FCM or OneSignal.
    Stub: returns True.
    """
    print(f"[PUSH STUB] To: {patient_id} | {title}: {body}")
    return True
