-- ============================================================
-- WellnessGPT — Supabase Schema
-- Run this in: Supabase Dashboard → SQL Editor → Run
-- ============================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ──────────────────────────────────────────────────────────────
-- Patients
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS patients (
    id                  TEXT PRIMARY KEY,
    name                TEXT NOT NULL,
    dob                 DATE NOT NULL,
    gender              TEXT CHECK (gender IN ('male', 'female', 'other')),
    blood_group         TEXT,
    allergies           TEXT[] DEFAULT '{}',
    chronic_conditions  TEXT[] DEFAULT '{}',
    abha_id             TEXT UNIQUE,
    phone               TEXT,
    email               TEXT,
    address             TEXT,
    emergency_contact   TEXT,
    family_id           TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Clinics
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS clinics (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    location    TEXT,
    departments TEXT[] DEFAULT '{}',
    contact     TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Doctors
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS doctors (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    specialty       TEXT NOT NULL,
    clinic_id       TEXT REFERENCES clinics(id),
    qualification   TEXT,
    available_days  TEXT[] DEFAULT '{}',
    available_times TEXT[] DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Appointments
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS appointments (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id       TEXT REFERENCES patients(id),
    doctor_id        TEXT REFERENCES doctors(id),
    specialty        TEXT,
    appointment_date DATE NOT NULL,
    slot_time        TEXT NOT NULL,
    status           TEXT DEFAULT 'scheduled' CHECK (status IN ('scheduled','completed','cancelled','no-show')),
    notes            TEXT,
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Symptoms / Triage Logs
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS symptoms_logs (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id              TEXT REFERENCES patients(id),
    symptoms                TEXT[] NOT NULL,
    urgency_level           TEXT CHECK (urgency_level IN ('low','medium','high','emergency')),
    recommended_specialty   TEXT,
    triage_notes            TEXT,
    is_emergency            BOOLEAN DEFAULT FALSE,
    created_at              TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Care Plans
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS care_plans (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id       TEXT REFERENCES patients(id),
    nutrition_plan   JSONB DEFAULT '{}',
    fitness_plan     JSONB DEFAULT '{}',
    preventive_care  TEXT[] DEFAULT '{}',
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    updated_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Prescriptions
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS prescriptions (
    id                    UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id            TEXT REFERENCES patients(id),
    doctor_id             TEXT REFERENCES doctors(id),
    medications           JSONB NOT NULL DEFAULT '[]',
    dosage_instructions   TEXT,
    created_at            TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Discharge Summaries
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS discharge_summaries (
    id                          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id                  TEXT REFERENCES patients(id),
    admission_date              DATE,
    discharge_date              DATE,
    diagnosis                   TEXT,
    summary                     TEXT,
    post_discharge_instructions TEXT[] DEFAULT '{}',
    follow_up_appointment_id    UUID,
    created_at                  TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Insurance Claims
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS insurance_claims (
    id               UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id       TEXT REFERENCES patients(id),
    policy_number    TEXT,
    insurer          TEXT,
    diagnosis        TEXT,
    treatment_cost   NUMERIC(12,2),
    coverage_amount  NUMERIC(12,2),
    coverage_gaps    TEXT[] DEFAULT '{}',
    wellness_score   NUMERIC(5,2) DEFAULT 0,
    status           TEXT DEFAULT 'pending' CHECK (status IN ('pending','approved','rejected','processing')),
    created_at       TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Hospital Beds
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hospital_beds (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id   TEXT REFERENCES clinics(id),
    ward        TEXT NOT NULL,
    bed_number  TEXT NOT NULL,
    status      TEXT DEFAULT 'available' CHECK (status IN ('available','occupied','maintenance')),
    patient_id  TEXT REFERENCES patients(id),
    updated_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Inventory
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS inventory (
    id             UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    clinic_id      TEXT REFERENCES clinics(id),
    item_name      TEXT NOT NULL,
    category       TEXT,
    quantity       INTEGER DEFAULT 0,
    reorder_level  INTEGER DEFAULT 10,
    unit           TEXT DEFAULT 'units',
    last_updated   TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Follow-up Reminders
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS followup_reminders (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id   TEXT REFERENCES patients(id),
    type         TEXT,
    message      TEXT,
    scheduled_at TIMESTAMPTZ,
    status       TEXT DEFAULT 'pending' CHECK (status IN ('pending','sent','acknowledged')),
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Mental Health Screenings
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS mental_health_screenings (
    id                 UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id         TEXT REFERENCES patients(id),
    phq9_score         INTEGER DEFAULT 0,
    gad7_score         INTEGER DEFAULT 0,
    risk_level         TEXT CHECK (risk_level IN ('low','moderate','high')),
    coping_strategies  TEXT[] DEFAULT '{}',
    escalate           BOOLEAN DEFAULT FALSE,
    created_at         TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Family Groups
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS family_groups (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    family_id   TEXT NOT NULL,
    patient_id  TEXT REFERENCES patients(id),
    UNIQUE(family_id, patient_id)
);

-- ──────────────────────────────────────────────────────────────
-- Nutrition Logs
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nutrition_logs (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id  TEXT REFERENCES patients(id),
    log_date    DATE DEFAULT CURRENT_DATE,
    meals       JSONB DEFAULT '[]',
    calories    INTEGER,
    adherence   BOOLEAN DEFAULT TRUE,
    notes       TEXT,
    created_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Fitness Logs
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS fitness_logs (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id          TEXT REFERENCES patients(id),
    log_date            DATE DEFAULT CURRENT_DATE,
    activity            TEXT,
    duration_minutes    INTEGER,
    calories_burned     INTEGER,
    notes               TEXT,
    created_at          TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Wearable Data
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS wearable_data (
    id           UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id   TEXT REFERENCES patients(id),
    device       TEXT DEFAULT 'fitbit',
    heart_rate   INTEGER,
    steps        INTEGER,
    sleep_hours  NUMERIC(4,2),
    spo2         NUMERIC(5,2),
    recorded_at  TIMESTAMPTZ DEFAULT NOW()
);

-- ──────────────────────────────────────────────────────────────
-- Patient Documents (PDF, Images, Reports)
-- ──────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS patient_documents (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    patient_id      TEXT REFERENCES patients(id),
    file_name       TEXT NOT NULL,
    file_type       TEXT, -- e.g. 'application/pdf', 'image/jpeg'
    bucket_name     TEXT NOT NULL,
    storage_path    TEXT NOT NULL,
    public_url      TEXT,
    metadata        JSONB DEFAULT '{}',
    created_at      TIMESTAMPTZ DEFAULT NOW()
);
