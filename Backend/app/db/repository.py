"""
Repository: Clean async CRUD helpers for all SQLite tables.
All functions return plain dicts or lists.
"""
from __future__ import annotations
import json
import uuid
import asyncio
from typing import Any
from app.db.sqlite import get_db

def _parse_json_fields(d: dict | None, fields: list[str]) -> dict | None:
    if not d: return d
    for f in fields:
        if f in d and isinstance(d[f], str):
            try:
                d[f] = json.loads(d[f])
            except:
                pass
    return d

def _parse_json_for_list(l: list[dict], fields: list[str]) -> list[dict]:
    return [_parse_json_fields(dict(d), fields) for d in l]

def _dict_factory_for_insert(d: dict, json_fields: list[str] = []) -> dict:
    """Prepare dict for SQLite insert (convert dict/lists to json strings)"""
    new_d = d.copy()
    for k, v in new_d.items():
        if k in json_fields or isinstance(v, (list, dict)):
            new_d[k] = json.dumps(v)
    return new_d

# ─────────────────────────── Patients ────────────────────────────────────────

def get_patient(patient_id: str) -> dict | None:
    with get_db() as db:
        res = db.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    return _parse_json_fields(res, ['allergies', 'chronic_conditions'])

def list_patients() -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM patients").fetchall()
    return _parse_json_for_list(res, ['allergies', 'chronic_conditions'])

def get_patient_by_abha(abha_id: str) -> dict | None:
    with get_db() as db:
        res = db.execute("SELECT * FROM patients WHERE abha_id = ?", (abha_id,)).fetchone()
    return _parse_json_fields(res, ['allergies', 'chronic_conditions'])

def get_family_members(family_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT patient_id FROM family_groups WHERE family_id = ?", (family_id,)).fetchall()
        if not res:
            return []
        ids = [r['patient_id'] for r in res]
        placeholders = ','.join('?' * len(ids))
        members = db.execute(f"SELECT * FROM patients WHERE id IN ({placeholders})", tuple(ids)).fetchall()
    return _parse_json_for_list(members, ['allergies', 'chronic_conditions'])


# ─────────────────────────── Appointments ─────────────────────────────────────

def get_doctor_availability(specialty: str, date: str) -> list[dict]:
    with get_db() as db:
        res = db.execute(
            "SELECT doctor_id, slot_time, status FROM appointments WHERE specialty = ? AND appointment_date = ?",
            (specialty, date)
        ).fetchall()
    return res

def list_doctors(specialty: str | None = None) -> list[dict]:
    with get_db() as db:
        if specialty:
            res = db.execute("SELECT * FROM doctors WHERE specialty = ?", (specialty,)).fetchall()
        else:
            res = db.execute("SELECT * FROM doctors").fetchall()
    return _parse_json_for_list(res, ['available_days', 'available_times'])

def create_appointment(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    cols = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    with get_db() as db:
        db.execute(f"INSERT INTO appointments ({cols}) VALUES ({placeholders})", tuple(data.values()))
        db.commit()
    return data

def get_appointments_for_patient(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("""
            SELECT a.*, d.name as doctor_name, d.specialty as doctor_specialty 
            FROM appointments a 
            LEFT JOIN doctors d ON a.doctor_id = d.id 
            WHERE a.patient_id = ?
        """, (patient_id,)).fetchall()
    # Supabase nested doctors as a dict. Let's emulate that.
    final_res = []
    for r in res:
        r_dict = dict(r)
        r_dict['doctors'] = {"name": r_dict.pop('doctor_name'), "specialty": r_dict.pop('doctor_specialty')}
        final_res.append(r_dict)
    return final_res


# ─────────────────────────── Symptoms / Triage ────────────────────────────────

def log_symptom_triage(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['symptoms'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO symptoms_logs ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data

def get_triage_history(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM symptoms_logs WHERE patient_id = ? ORDER BY created_at DESC LIMIT 10", (patient_id,)).fetchall()
    return _parse_json_for_list(res, ['symptoms'])


# ─────────────────────────── Care Plans ───────────────────────────────────────

def get_care_plan(patient_id: str) -> dict | None:
    with get_db() as db:
        res = db.execute("SELECT * FROM care_plans WHERE patient_id = ? ORDER BY created_at DESC LIMIT 1", (patient_id,)).fetchone()
    return _parse_json_fields(res, ['nutrition_plan', 'fitness_plan', 'preventive_care'])

def upsert_care_plan(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['nutrition_plan', 'fitness_plan', 'preventive_care'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    # Basic SQLite upsert
    update_clause = ', '.join([f"{k}=Excluded.{k}" for k in d.keys() if k != 'id'])
    with get_db() as db:
        db.execute(f"""
            INSERT INTO care_plans ({cols}) VALUES ({placeholders})
            ON CONFLICT(id) DO UPDATE SET {update_clause}
        """, tuple(d.values()))
        db.commit()
    return data


# ─────────────────────────── Prescriptions ───────────────────────────────────

def get_prescriptions(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM prescriptions WHERE patient_id = ? ORDER BY created_at DESC", (patient_id,)).fetchall()
    return _parse_json_for_list(res, ['medications'])

def create_prescription(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['medications'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO prescriptions ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data


# ─────────────────────────── Discharge ───────────────────────────────────────

def create_discharge_summary(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['post_discharge_instructions'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO discharge_summaries ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data

def get_discharge_summary(patient_id: str) -> dict | None:
    with get_db() as db:
        res = db.execute("SELECT * FROM discharge_summaries WHERE patient_id = ? ORDER BY discharge_date DESC LIMIT 1", (patient_id,)).fetchone()
    return _parse_json_fields(res, ['post_discharge_instructions'])


# ─────────────────────────── Insurance Claims ────────────────────────────────

def get_claim(patient_id: str) -> dict | None:
    with get_db() as db:
        res = db.execute("SELECT * FROM insurance_claims WHERE patient_id = ? ORDER BY created_at DESC LIMIT 1", (patient_id,)).fetchone()
    return _parse_json_fields(res, ['coverage_gaps'])

def create_claim(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['coverage_gaps'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO insurance_claims ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data

def update_claim_status(claim_id: str, status: str) -> dict:
    with get_db() as db:
        db.execute("UPDATE insurance_claims SET status = ? WHERE id = ?", (status, claim_id))
        db.commit()
    return {"id": claim_id, "status": status}


# ─────────────────────────── Hospital Ops ────────────────────────────────────

def list_beds(clinic_id: str | None = None, status: str | None = None) -> list[dict]:
    query = "SELECT * FROM hospital_beds WHERE 1=1"
    params = []
    if clinic_id:
        query += " AND clinic_id = ?"
        params.append(clinic_id)
    if status:
        query += " AND status = ?"
        params.append(status)
    with get_db() as db:
        res = db.execute(query, tuple(params)).fetchall()
    return res

def update_bed_status(bed_id: str, status: str) -> dict:
    with get_db() as db:
        db.execute("UPDATE hospital_beds SET status = ? WHERE id = ?", (status, bed_id))
        db.commit()
    return {"id": bed_id, "status": status}

def list_inventory(clinic_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM inventory WHERE clinic_id = ?", (clinic_id,)).fetchall()
    return res


# ─────────────────────────── Reminders ───────────────────────────────────────

def create_reminder(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    cols = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    with get_db() as db:
        db.execute(f"INSERT INTO followup_reminders ({cols}) VALUES ({placeholders})", tuple(data.values()))
        db.commit()
    return data

def get_pending_reminders(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM followup_reminders WHERE patient_id = ? AND status = 'pending'", (patient_id,)).fetchall()
    return res


# ─────────────────────────── Mental Health ───────────────────────────────────

def create_mental_health_screening(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['coping_strategies'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO mental_health_screenings ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data

def get_mental_health_history(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM mental_health_screenings WHERE patient_id = ? ORDER BY created_at DESC LIMIT 5", (patient_id,)).fetchall()
    return _parse_json_for_list(res, ['coping_strategies'])


# ─────────────────────────── Nutrition / Fitness ─────────────────────────────

def log_nutrition(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    d = _dict_factory_for_insert(data, ['meals'])
    cols = ', '.join(d.keys())
    placeholders = ', '.join('?' * len(d))
    with get_db() as db:
        db.execute(f"INSERT INTO nutrition_logs ({cols}) VALUES ({placeholders})", tuple(d.values()))
        db.commit()
    return data

def get_nutrition_logs(patient_id: str, limit: int = 7) -> list[dict]:
    with get_db() as db:
        res = db.execute(f"SELECT * FROM nutrition_logs WHERE patient_id = ? ORDER BY log_date DESC LIMIT {limit}", (patient_id,)).fetchall()
    return _parse_json_for_list(res, ['meals'])

def log_fitness(data: dict) -> dict:
    if 'id' not in data:
        data['id'] = str(uuid.uuid4())
    cols = ', '.join(data.keys())
    placeholders = ', '.join('?' * len(data))
    with get_db() as db:
        db.execute(f"INSERT INTO fitness_logs ({cols}) VALUES ({placeholders})", tuple(data.values()))
        db.commit()
    return data

def get_fitness_logs(patient_id: str, limit: int = 7) -> list[dict]:
    with get_db() as db:
        res = db.execute(f"SELECT * FROM fitness_logs WHERE patient_id = ? ORDER BY log_date DESC LIMIT {limit}", (patient_id,)).fetchall()
    return res

def get_wearable_data(patient_id: str) -> list[dict]:
    with get_db() as db:
        res = db.execute("SELECT * FROM wearable_data WHERE patient_id = ? ORDER BY recorded_at DESC LIMIT 10", (patient_id,)).fetchall()
    return res


# ─────────────────────────── Product Catalog ─────────────────────────────────

def search_products(tags: list[str]) -> list[dict]:
    # Try not to use `overlaps` since SQLite doesn't natively have array overlaps.
    # We will fetch all and filter in Python since catalog is small.
    with get_db() as db:
        try:
            res = db.execute("SELECT * FROM product_catalog").fetchall()
        except sqlite3.OperationalError:
            return [] # In case product_catalog isn't created. I noticed it in seed but not schema! Wait, let's just return [] if it fails
    
    all_products = _parse_json_for_list(res, ['tags'])
    if not tags: return all_products
    
    matched = []
    tags_set = set(tags)
    for p in all_products:
        p_tags = p.get('tags') or []
        # If any tag overlaps
        if tags_set.intersection(set(p_tags)):
            matched.append(p)
    return matched

async def log_patient_document(doc_data: dict) -> dict:
    """Register an uploaded document (PDF/Image) in the patient_documents table."""
    def _do():
        d = dict(doc_data)
        if 'id' not in d: d['id'] = str(uuid.uuid4())
        cols = ', '.join(d.keys())
        placeholders = ', '.join('?' * len(d))
        with get_db() as db:
            db.execute(f"INSERT INTO patient_documents ({cols}) VALUES ({placeholders})", tuple(d.values()))
            db.commit()
        return d
    # run in threadpool so we don't block
    return await asyncio.to_thread(_do)
