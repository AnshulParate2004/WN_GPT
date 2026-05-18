-- ============================================================
-- WellnessGPT — SQLite Demo Seed Data
-- ============================================================

-- ── Clinics ──────────────────────────────────────────────────
INSERT OR IGNORE INTO clinics (id, name, location, departments, contact) VALUES
('CLN001', 'Clearmedi Central Hospital', 'Bandra, Mumbai', '["cardiology","orthopedics","neurology","general_medicine","icu"]', '+91-22-40001234'),
('CLN002', 'Clearmedi Wellness Hub', 'Koregaon Park, Pune', '["psychiatry","dermatology","endocrinology","gynecology","pediatrics"]', '+91-20-65009999'),
('CLN003', 'Clearmedi Diagnostics', 'Whitefield, Bangalore', '["radiology","pathology","general_medicine","pulmonology","gastroenterology"]', '+91-80-43210000');

-- ── Doctors ─────────────────────────────────────────────────
INSERT OR IGNORE INTO doctors (id, name, specialty, clinic_id, qualification, available_days, available_times) VALUES
('DOC001', 'Dr. Priya Sharma',    'cardiology',       'CLN001', 'MD, DM Cardiology',    '["Monday","Wednesday","Friday"]', '["09:00","10:00","11:00","14:00","15:00"]'),
('DOC002', 'Dr. Arjun Mehta',     'orthopedics',      'CLN001', 'MS Orthopedics',        '["Tuesday","Thursday","Saturday"]', '["10:00","11:00","16:00","17:00"]'),
('DOC003', 'Dr. Neha Iyer',       'psychiatry',       'CLN002', 'MD Psychiatry',         '["Monday","Tuesday","Thursday"]', '["09:00","10:00","11:00","15:00"]'),
('DOC004', 'Dr. Sameer Joshi',    'endocrinology',    'CLN002', 'MD, DM Endocrinology',  '["Wednesday","Friday"]', '["10:00","11:00","14:00","15:00","16:00"]'),
('DOC005', 'Dr. Kavitha Rao',     'neurology',        'CLN001', 'MD, DM Neurology',      '["Monday","Wednesday","Friday"]', '["09:00","10:00","14:00","15:00"]'),
('DOC006', 'Dr. Rohan Desai',     'pulmonology',      'CLN003', 'MD Pulmonology, FCCP',  '["Tuesday","Thursday"]', '["09:00","10:00","11:00","12:00"]'),
('DOC007', 'Dr. Ananya Singh',    'gynecology',       'CLN002', 'MS Gynecology & Obs',   '["Monday","Wednesday","Saturday"]', '["09:00","10:00","11:00","15:00"]'),
('DOC008', 'Dr. Vikram Nair',     'general_medicine', 'CLN003', 'MBBS, MD General Med',  '["Monday","Tuesday","Wednesday","Thursday","Friday"]', '["09:00","10:00","11:00","12:00","14:00","15:00"]');

-- ── Patients ─────────────────────────────────────────────────
INSERT OR IGNORE INTO patients (id, name, dob, gender, blood_group, allergies, chronic_conditions, abha_id, phone, email, address, emergency_contact, family_id) VALUES
('P001', 'Rahul Verma',    '1985-06-15', 'male',   'O+', '["penicillin"]',               '["hypertension","type2_diabetes"]',  'ABHA-P001-2024', '+91-9876543210', 'rahul.verma@email.com',   'Andheri East, Mumbai',   '+91-9876543211', 'FAM001'),
('P002', 'Sunita Verma',   '1988-03-22', 'female', 'A+', '[]',                   '["hypothyroidism"]',                 'ABHA-P002-2024', '+91-9876543212', 'sunita.verma@email.com',  'Andheri East, Mumbai',   '+91-9876543210', 'FAM001'),
('P003', 'Aditya Verma',   '2012-11-05', 'male',   'O+', '["dust_allergy"]',             '["asthma"]',                         'ABHA-P003-2024', '+91-9876543213', 'aditya.verma@email.com',  'Andheri East, Mumbai',   '+91-9876543210', 'FAM001'),
('P004', 'Meera Krishnan', '1972-08-30', 'female', 'B+', '["sulfa_drugs","shellfish"]',  '["rheumatoid_arthritis","anemia"]',  'ABHA-P004-2024', '+91-9988776655', 'meera.k@email.com',       'Koregaon Park, Pune',    '+91-9988776656', 'FAM002'),
('P005', 'Suresh Pillai',  '1965-01-18', 'male',   'AB+','["aspirin"]',                  '["coronary_artery_disease","copd"]','ABHA-P005-2024', '+91-9123456789', 'suresh.p@email.com',      'Whitefield, Bangalore',  '+91-9123456790', 'FAM003');

-- ── Family Groups ────────────────────────────────────────────
INSERT OR IGNORE INTO family_groups (id, family_id, patient_id) VALUES
('FG001', 'FAM001', 'P001'), ('FG002', 'FAM001', 'P002'), ('FG003', 'FAM001', 'P003'),
('FG004', 'FAM002', 'P004'),
('FG005', 'FAM003', 'P005');

-- ── Appointments ─────────────────────────────────────────────
INSERT OR IGNORE INTO appointments (id, patient_id, doctor_id, specialty, appointment_date, slot_time, status, notes) VALUES
('APP001', 'P001', 'DOC001', 'cardiology',    '2026-03-28', '09:00', 'scheduled',  'Routine cardiac checkup'),
('APP002', 'P001', 'DOC008', 'general_medicine','2026-03-20','10:00','completed', 'Annual health check'),
('APP003', 'P002', 'DOC004', 'endocrinology', '2026-03-29', '14:00', 'scheduled',  'Thyroid follow-up'),
('APP004', 'P003', 'DOC006', 'pulmonology',   '2026-03-30', '09:00', 'scheduled',  'Asthma management review'),
('APP005', 'P004', 'DOC002', 'orthopedics',   '2026-03-27', '10:00', 'scheduled',  'RA joint assessment'),
('APP006', 'P005', 'DOC001', 'cardiology',    '2026-04-02', '14:00', 'scheduled',  'CAD monitoring + ECG'),
('APP007', 'P005', 'DOC006', 'pulmonology',   '2026-04-03', '09:00', 'scheduled',  'COPD spirometry');

-- ── Symptom Triage Logs ──────────────────────────────────────
INSERT OR IGNORE INTO symptoms_logs (id, patient_id, symptoms, urgency_level, recommended_specialty, triage_notes, is_emergency) VALUES
('SYM001', 'P001', '["chest pain","shortness of breath","sweating"]', 'high',      'cardiology',    'Possible angina or ACS. Requires immediate cardiac evaluation. ECG and troponin recommended.', 0),
('SYM002', 'P004', '["severe joint pain","swelling","morning stiffness"]', 'medium','orthopedics',  'RA flare-up likely. CBC and CRP indicated. Adjust DMARDs if necessary.', 0),
('SYM003', 'P005', '["severe breathlessness","persistent cough","chest tightness"]', 'emergency','pulmonology','COPD exacerbation. Immediate bronchodilator therapy. O2 saturation critically low.', 1),
('SYM004', 'P002', '["fatigue","weight gain","cold intolerance"]', 'low',           'endocrinology', 'Consistent with hypothyroidism. TSH, T3, T4 levels recommended.', 0),
('SYM005', 'P003', '["wheezing","nighttime cough","difficulty breathing"]', 'medium','pulmonology',  'Asthma symptoms. Check peak flow. Consider inhaler adjustment.', 0);

-- ── Care Plans ───────────────────────────────────────────────
INSERT OR IGNORE INTO care_plans (id, patient_id, nutrition_plan, fitness_plan, preventive_care) VALUES
('CP001', 'P001',
 '{"daily_calories": 1800, "meals": ["Oats + skimmed milk breakfast", "Grilled chicken salad lunch", "Dal + roti + sabzi dinner"], "restrictions": ["low sodium", "low fat", "no processed food"], "hydration_goal_liters": 2.5}',
 '{"weekly_sessions": 5, "session_duration_minutes": 30, "recommended_activities": ["brisk walking", "yoga", "swimming"], "intensity": "moderate"}',
 '["Annual ECG", "Blood pressure monitoring daily", "HbA1c every 3 months", "Eye checkup annually", "Foot care for diabetes"]'),
('CP002', 'P005',
 '{"daily_calories": 1600, "meals": ["Soft idli + coconut chutney breakfast", "Brown rice + rasam lunch", "Steamed vegetables + roti dinner"], "restrictions": ["low sodium", "no spicy food", "low fat"], "hydration_goal_liters": 2.0}',
 '{"weekly_sessions": 3, "session_duration_minutes": 20, "recommended_activities": ["slow walking", "breathing exercises", "light yoga"], "intensity": "low"}',
 '["Spirometry every 6 months", "Annual chest X-ray", "Flu vaccination", "Pneumococcal vaccine", "Cardiac stress test annually"]');

-- ── Prescriptions ────────────────────────────────────────────
INSERT OR IGNORE INTO prescriptions (id, patient_id, doctor_id, medications, dosage_instructions) VALUES
('PR001', 'P001', 'DOC001', '[{"name":"Metformin","dose":"500mg","frequency":"twice daily"},{"name":"Amlodipine","dose":"5mg","frequency":"once daily"},{"name":"Aspirin","dose":"75mg","frequency":"once daily"}]', 'Take Metformin with meals. Amlodipine in the morning. Aspirin at night.'),
('PR002', 'P002', 'DOC004', '[{"name":"Levothyroxine","dose":"50mcg","frequency":"once daily, empty stomach"}]', 'Take 30 minutes before breakfast. Do not take with calcium or iron supplements.'),
('PR003', 'P004', 'DOC002', '[{"name":"Methotrexate","dose":"15mg","frequency":"once weekly"},{"name":"Folic Acid","dose":"5mg","frequency":"once weekly (day after MTX)"},{"name":"Hydroxychloroquine","dose":"200mg","frequency":"twice daily"}]', 'Take MTX on Sunday evenings. Folic acid on Monday. Regular LFT monitoring required.'),
('PR004', 'P005', 'DOC001', '[{"name":"Atorvastatin","dose":"40mg","frequency":"once daily at night"},{"name":"Clopidogrel","dose":"75mg","frequency":"once daily"},{"name":"Bisoprolol","dose":"5mg","frequency":"once daily"}]', 'Atorvastatin at bedtime. Monitor LFT quarterly. Do not stop Clopidogrel without doctor advice.');

-- ── Hospital Beds ────────────────────────────────────────────
INSERT OR IGNORE INTO hospital_beds (id, clinic_id, ward, bed_number, status, patient_id) VALUES
('BED001', 'CLN001', 'Cardiac ICU',  'BED-C01', 'occupied',    'P005'),
('BED002', 'CLN001', 'Cardiac ICU',  'BED-C02', 'available',   NULL),
('BED003', 'CLN001', 'General Ward', 'BED-G01', 'available',   NULL),
('BED004', 'CLN001', 'General Ward', 'BED-G02', 'occupied',    'P001'),
('BED005', 'CLN001', 'General Ward', 'BED-G03', 'maintenance', NULL),
('BED006', 'CLN002', 'General Ward', 'BED-G01', 'available',   NULL),
('BED007', 'CLN002', 'General Ward', 'BED-G02', 'available',   NULL),
('BED008', 'CLN003', 'General Ward', 'BED-G01', 'occupied',    'P003');

-- ── Inventory ────────────────────────────────────────────────
INSERT OR IGNORE INTO inventory (id, clinic_id, item_name, category, quantity, reorder_level, unit) VALUES
('INV001', 'CLN001', 'Oxygen Cylinders',       'medical_gas',    15, 10, 'cylinders'),
('INV002', 'CLN001', 'Surgical Gloves (L)',    'ppe',             250, 100, 'pairs'),
('INV003', 'CLN001', 'N95 Masks',              'ppe',              8, 50, 'units'),
('INV004', 'CLN001', 'Paracetamol 500mg',      'medication',     500, 200, 'tablets'),
('INV005', 'CLN001', 'IV Normal Saline 500ml', 'iv_fluids',       30, 20, 'bags'),
('INV006', 'CLN002', 'Antidepressants SSRIs',  'medication',      40, 30, 'strips'),
('INV007', 'CLN002', 'Blood Glucose Strips',   'diagnostics',      5, 50, 'strips'),
('INV008', 'CLN003', 'Salbutamol Inhaler',     'medication',      12,  5, 'units'),
('INV009', 'CLN003', 'Spirometer Filters',     'diagnostics',      3, 10, 'units');

-- ── Follow-up Reminders ──────────────────────────────────────
INSERT OR IGNORE INTO followup_reminders (id, patient_id, type, message, scheduled_at, status) VALUES
('FR001', 'P001', 'medication', 'Time to take your evening Metformin and Aspirin!', datetime('now', '+6 hours'), 'pending'),
('FR002', 'P001', 'appointment', 'Your cardiology appointment is tomorrow at 9:00 AM with Dr. Priya Sharma.', datetime('now', '+20 hours'), 'pending'),
('FR003', 'P002', 'medication', 'Remember to take Levothyroxine 30 minutes before breakfast tomorrow.', datetime('now', '+14 hours'), 'pending'),
('FR004', 'P004', 'medication', 'Tonight is your weekly Methotrexate dose. Stay hydrated!', datetime('now', '+4 hours'), 'pending'),
('FR005', 'P005', 'checkup', 'Monthly cardiac check-in: please log your current symptoms and send BP readings.', datetime('now', '+2 hours'), 'pending');

-- ── Mental Health Screenings ─────────────────────────────────
INSERT OR IGNORE INTO mental_health_screenings (id, patient_id, phq9_score, gad7_score, risk_level, coping_strategies, escalate) VALUES
('MHS001', 'P001', 6, 5, 'low',      '["daily meditation 10 min","journaling","regular sleep schedule"]', 0),
('MHS002', 'P004', 12, 9, 'moderate', '["mindfulness app","CBT exercises","social support group","gentle yoga"]', 0),
('MHS003', 'P005', 15, 11, 'high',   '["professional counseling","breathing exercises","limit news consumption"]', 1);

-- ── Wearable Data ────────────────────────────────────────────
INSERT OR IGNORE INTO wearable_data (id, patient_id, device, heart_rate, steps, sleep_hours, spo2) VALUES
('WD001', 'P001', 'fitbit', 82, 6200, 6.5, 98.0),
('WD002', 'P001', 'fitbit', 88, 4500, 5.8, 97.5),
('WD003', 'P005', 'fitbit', 95, 1200, 5.0, 91.0),
('WD004', 'P005', 'fitbit', 98, 800,  4.5, 89.5),
('WD005', 'P003', 'apple_health', 85, 3000, 8.0, 96.0),
('WD006', 'P002', 'fitbit', 72, 7800, 7.0, 99.0);

-- ── Nutrition Logs ───────────────────────────────────────────
INSERT OR IGNORE INTO nutrition_logs (id, patient_id, log_date, meals, calories, adherence, notes) VALUES
('NL001', 'P001', date('now', '-1 day'), '[{"meal":"breakfast","food":"oats + milk"},{"meal":"lunch","food":"grilled chicken salad"},{"meal":"dinner","food":"dal + 2 rotis"}]', 1750, 1,  'Good adherence today'),
('NL002', 'P001', date('now'),     '[{"meal":"breakfast","food":"oats + milk"},{"meal":"lunch","food":"biryani (cheat)"}]', 2100, 0, 'Ate out for lunch — high calorie'),
('NL003', 'P005', date('now', '-1 day'), '[{"meal":"breakfast","food":"idli x4"},{"meal":"lunch","food":"brown rice + rasam"}]', 1500, 1,  'Good portions, low sodium');

-- ── Fitness Logs ─────────────────────────────────────────────
INSERT OR IGNORE INTO fitness_logs (id, patient_id, log_date, activity, duration_minutes, calories_burned, notes) VALUES
('FL001', 'P001', date('now', '-1 day'), 'brisk walking', 30, 180, 'Morning walk at park'),
('FL002', 'P001', date('now', '-2 days'), 'yoga',          25, 120, 'Online yoga session'),
('FL003', 'P002', date('now', '-1 day'), 'walking',       20,  90, 'Evening stroll'),
('FL004', 'P005', date('now', '-1 day'), 'breathing exercises', 15, 40, 'Pursed lip breathing + diaphragmatic exercises');

-- ── Product Catalog ──────────────────────────────────────────
INSERT OR IGNORE INTO product_catalog (id, name, category, partner, description, tags, price_inr) VALUES
('PROD001', 'Omega-3 Fish Oil 1000mg',         'supplement', 'HealthVit',       'EPA + DHA for cardiac health',                       '["cardiac","cholesterol","heart"]',               799),
('PROD002', 'Vitamin D3 + K2 Drops',           'supplement', 'Healthkart',      'Bone health and immunity support',                   '["bones","immunity","vitamin_d"]',                599),
('PROD003', 'Magnesium Glycinate 400mg',        'supplement', 'NOW Foods India', 'Sleep quality and muscle relaxation',                '["sleep","stress","anxiety","muscle"]',           999),
('PROD004', 'CGM Continuous Glucose Monitor',  'device',     'Dexcom India',    '14-day real-time glucose tracking for diabetics',    '["diabetes","glucose","monitoring"]',            4999),
('PROD005', 'Spirometer for Home Use',         'device',     'Nidek Medical',   'Personal peak flow monitoring for COPD/Asthma',      '["copd","asthma","pulmonology","breathing"]',    2499),
('PROD006', 'Yoga Mat Premium',                'fitness',    'Decathlon India', 'Anti-slip 6mm yoga mat for home workouts',           '["fitness","yoga","stress"]',                     899),
('PROD007', 'Ayurvedic Arthritis Oil',         'supplement', 'Zandu',           'Joint pain relief oil with Ayurvedic formulation',   '["arthritis","joint_pain","orthopedics"]',        349),
('PROD008', 'Mental Wellness App - 1 Year',    'service',    'Wysa',            'AI + human therapist hybrid mental health support',  '["mental_health","anxiety","depression"]',        2999),
('PROD009', 'Diabetic Care Pack',              'supplement', 'HealthVit',       'Chromium, Alpha lipoic acid, Bitter melon extract',  '["diabetes","glucose","insulin_sensitivity"]',    1299),
('PROD010', 'HEPA Air Purifier For Bedroom',   'device',     'Dyson India',     'Removes allergens, pollutants — ideal for asthma',   '["asthma","allergy","pulmonology","air"]',       18999);
