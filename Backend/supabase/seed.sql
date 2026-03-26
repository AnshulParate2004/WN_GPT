-- ============================================================
-- WellnessGPT — Demo Seed Data
-- Run AFTER schema.sql
-- ============================================================

-- ── Clinics ──────────────────────────────────────────────────
INSERT INTO clinics (id, name, location, departments, contact) VALUES
('CLN001', 'Clearmedi Central Hospital', 'Bandra, Mumbai', ARRAY['cardiology','orthopedics','neurology','general_medicine','icu'], '+91-22-40001234'),
('CLN002', 'Clearmedi Wellness Hub', 'Koregaon Park, Pune', ARRAY['psychiatry','dermatology','endocrinology','gynecology','pediatrics'], '+91-20-65009999'),
('CLN003', 'Clearmedi Diagnostics', 'Whitefield, Bangalore', ARRAY['radiology','pathology','general_medicine','pulmonology','gastroenterology'], '+91-80-43210000')
ON CONFLICT (id) DO NOTHING;

-- ── Doctors ─────────────────────────────────────────────────
INSERT INTO doctors (id, name, specialty, clinic_id, qualification, available_days, available_times) VALUES
('DOC001', 'Dr. Priya Sharma',    'cardiology',       'CLN001', 'MD, DM Cardiology',    ARRAY['Monday','Wednesday','Friday'], ARRAY['09:00','10:00','11:00','14:00','15:00']),
('DOC002', 'Dr. Arjun Mehta',     'orthopedics',      'CLN001', 'MS Orthopedics',        ARRAY['Tuesday','Thursday','Saturday'], ARRAY['10:00','11:00','16:00','17:00']),
('DOC003', 'Dr. Neha Iyer',       'psychiatry',       'CLN002', 'MD Psychiatry',         ARRAY['Monday','Tuesday','Thursday'], ARRAY['09:00','10:00','11:00','15:00']),
('DOC004', 'Dr. Sameer Joshi',    'endocrinology',    'CLN002', 'MD, DM Endocrinology',  ARRAY['Wednesday','Friday'], ARRAY['10:00','11:00','14:00','15:00','16:00']),
('DOC005', 'Dr. Kavitha Rao',     'neurology',        'CLN001', 'MD, DM Neurology',      ARRAY['Monday','Wednesday','Friday'], ARRAY['09:00','10:00','14:00','15:00']),
('DOC006', 'Dr. Rohan Desai',     'pulmonology',      'CLN003', 'MD Pulmonology, FCCP',  ARRAY['Tuesday','Thursday'], ARRAY['09:00','10:00','11:00','12:00']),
('DOC007', 'Dr. Ananya Singh',    'gynecology',       'CLN002', 'MS Gynecology & Obs',   ARRAY['Monday','Wednesday','Saturday'], ARRAY['09:00','10:00','11:00','15:00']),
('DOC008', 'Dr. Vikram Nair',     'general_medicine', 'CLN003', 'MBBS, MD General Med',  ARRAY['Monday','Tuesday','Wednesday','Thursday','Friday'], ARRAY['09:00','10:00','11:00','12:00','14:00','15:00'])
ON CONFLICT (id) DO NOTHING;

-- ── Patients ─────────────────────────────────────────────────
INSERT INTO patients (id, name, dob, gender, blood_group, allergies, chronic_conditions, abha_id, phone, email, address, emergency_contact, family_id) VALUES
('P001', 'Rahul Verma',    '1985-06-15', 'male',   'O+', ARRAY['penicillin'],               ARRAY['hypertension','type2_diabetes'],  'ABHA-P001-2024', '+91-9876543210', 'rahul.verma@email.com',   'Andheri East, Mumbai',   '+91-9876543211', 'FAM001'),
('P002', 'Sunita Verma',   '1988-03-22', 'female', 'A+', ARRAY[]::TEXT[],                   ARRAY['hypothyroidism'],                 'ABHA-P002-2024', '+91-9876543212', 'sunita.verma@email.com',  'Andheri East, Mumbai',   '+91-9876543210', 'FAM001'),
('P003', 'Aditya Verma',   '2012-11-05', 'male',   'O+', ARRAY['dust_allergy'],             ARRAY['asthma'],                         'ABHA-P003-2024', '+91-9876543213', 'aditya.verma@email.com',  'Andheri East, Mumbai',   '+91-9876543210', 'FAM001'),
('P004', 'Meera Krishnan', '1972-08-30', 'female', 'B+', ARRAY['sulfa_drugs','shellfish'],  ARRAY['rheumatoid_arthritis','anemia'],  'ABHA-P004-2024', '+91-9988776655', 'meera.k@email.com',       'Koregaon Park, Pune',    '+91-9988776656', 'FAM002'),
('P005', 'Suresh Pillai',  '1965-01-18', 'male',   'AB+',ARRAY['aspirin'],                  ARRAY['coronary_artery_disease','copd'],'ABHA-P005-2024', '+91-9123456789', 'suresh.p@email.com',      'Whitefield, Bangalore',  '+91-9123456790', 'FAM003')
ON CONFLICT (id) DO NOTHING;

-- ── Family Groups ────────────────────────────────────────────
INSERT INTO family_groups (family_id, patient_id) VALUES
('FAM001', 'P001'), ('FAM001', 'P002'), ('FAM001', 'P003'),
('FAM002', 'P004'),
('FAM003', 'P005')
ON CONFLICT (family_id, patient_id) DO NOTHING;

-- ── Appointments ─────────────────────────────────────────────
INSERT INTO appointments (patient_id, doctor_id, specialty, appointment_date, slot_time, status, notes) VALUES
('P001', 'DOC001', 'cardiology',    '2026-03-28', '09:00', 'scheduled',  'Routine cardiac checkup'),
('P001', 'DOC008', 'general_medicine','2026-03-20','10:00','completed', 'Annual health check'),
('P002', 'DOC004', 'endocrinology', '2026-03-29', '14:00', 'scheduled',  'Thyroid follow-up'),
('P003', 'DOC006', 'pulmonology',   '2026-03-30', '09:00', 'scheduled',  'Asthma management review'),
('P004', 'DOC002', 'orthopedics',   '2026-03-27', '10:00', 'scheduled',  'RA joint assessment'),
('P005', 'DOC001', 'cardiology',    '2026-04-02', '14:00', 'scheduled',  'CAD monitoring + ECG'),
('P005', 'DOC006', 'pulmonology',   '2026-04-03', '09:00', 'scheduled',  'COPD spirometry');

-- ── Symptom Triage Logs ──────────────────────────────────────
INSERT INTO symptoms_logs (patient_id, symptoms, urgency_level, recommended_specialty, triage_notes, is_emergency) VALUES
('P001', ARRAY['chest pain','shortness of breath','sweating'], 'high',      'cardiology',    'Possible angina or ACS. Requires immediate cardiac evaluation. ECG and troponin recommended.', FALSE),
('P004', ARRAY['severe joint pain','swelling','morning stiffness'], 'medium','orthopedics',  'RA flare-up likely. CBC and CRP indicated. Adjust DMARDs if necessary.', FALSE),
('P005', ARRAY['severe breathlessness','persistent cough','chest tightness'], 'emergency','pulmonology','COPD exacerbation. Immediate bronchodilator therapy. O2 saturation critically low.', TRUE),
('P002', ARRAY['fatigue','weight gain','cold intolerance'], 'low',           'endocrinology', 'Consistent with hypothyroidism. TSH, T3, T4 levels recommended.', FALSE),
('P003', ARRAY['wheezing','nighttime cough','difficulty breathing'], 'medium','pulmonology',  'Asthma symptoms. Check peak flow. Consider inhaler adjustment.', FALSE);

-- ── Care Plans ───────────────────────────────────────────────
INSERT INTO care_plans (patient_id, nutrition_plan, fitness_plan, preventive_care) VALUES
('P001',
 '{"daily_calories": 1800, "meals": ["Oats + skimmed milk breakfast", "Grilled chicken salad lunch", "Dal + roti + sabzi dinner"], "restrictions": ["low sodium", "low fat", "no processed food"], "hydration_goal_liters": 2.5}',
 '{"weekly_sessions": 5, "session_duration_minutes": 30, "recommended_activities": ["brisk walking", "yoga", "swimming"], "intensity": "moderate"}',
 ARRAY['Annual ECG', 'Blood pressure monitoring daily', 'HbA1c every 3 months', 'Eye checkup annually', 'Foot care for diabetes']),
('P005',
 '{"daily_calories": 1600, "meals": ["Soft idli + coconut chutney breakfast", "Brown rice + rasam lunch", "Steamed vegetables + roti dinner"], "restrictions": ["low sodium", "no spicy food", "low fat"], "hydration_goal_liters": 2.0}',
 '{"weekly_sessions": 3, "session_duration_minutes": 20, "recommended_activities": ["slow walking", "breathing exercises", "light yoga"], "intensity": "low"}',
 ARRAY['Spirometry every 6 months', 'Annual chest X-ray', 'Flu vaccination', 'Pneumococcal vaccine', 'Cardiac stress test annually']);

-- ── Prescriptions ────────────────────────────────────────────
INSERT INTO prescriptions (patient_id, doctor_id, medications, dosage_instructions) VALUES
('P001', 'DOC001', '[{"name":"Metformin","dose":"500mg","frequency":"twice daily"},{"name":"Amlodipine","dose":"5mg","frequency":"once daily"},{"name":"Aspirin","dose":"75mg","frequency":"once daily"}]', 'Take Metformin with meals. Amlodipine in the morning. Aspirin at night.'),
('P002', 'DOC004', '[{"name":"Levothyroxine","dose":"50mcg","frequency":"once daily, empty stomach"}]', 'Take 30 minutes before breakfast. Do not take with calcium or iron supplements.'),
('P004', 'DOC002', '[{"name":"Methotrexate","dose":"15mg","frequency":"once weekly"},{"name":"Folic Acid","dose":"5mg","frequency":"once weekly (day after MTX)"},{"name":"Hydroxychloroquine","dose":"200mg","frequency":"twice daily"}]', 'Take MTX on Sunday evenings. Folic acid on Monday. Regular LFT monitoring required.'),
('P005', 'DOC001', '[{"name":"Atorvastatin","dose":"40mg","frequency":"once daily at night"},{"name":"Clopidogrel","dose":"75mg","frequency":"once daily"},{"name":"Bisoprolol","dose":"5mg","frequency":"once daily"}]', 'Atorvastatin at bedtime. Monitor LFT quarterly. Do not stop Clopidogrel without doctor advice.');

-- ── Hospital Beds ────────────────────────────────────────────
INSERT INTO hospital_beds (clinic_id, ward, bed_number, status, patient_id) VALUES
('CLN001', 'Cardiac ICU',  'BED-C01', 'occupied',    'P005'),
('CLN001', 'Cardiac ICU',  'BED-C02', 'available',   NULL),
('CLN001', 'General Ward', 'BED-G01', 'available',   NULL),
('CLN001', 'General Ward', 'BED-G02', 'occupied',    'P001'),
('CLN001', 'General Ward', 'BED-G03', 'maintenance', NULL),
('CLN002', 'General Ward', 'BED-G01', 'available',   NULL),
('CLN002', 'General Ward', 'BED-G02', 'available',   NULL),
('CLN003', 'General Ward', 'BED-G01', 'occupied',    'P003');

-- ── Inventory ────────────────────────────────────────────────
INSERT INTO inventory (clinic_id, item_name, category, quantity, reorder_level, unit) VALUES
('CLN001', 'Oxygen Cylinders',       'medical_gas',    15, 10, 'cylinders'),
('CLN001', 'Surgical Gloves (L)',    'ppe',             250, 100, 'pairs'),
('CLN001', 'N95 Masks',              'ppe',              8, 50, 'units'),      -- LOW STOCK
('CLN001', 'Paracetamol 500mg',      'medication',     500, 200, 'tablets'),
('CLN001', 'IV Normal Saline 500ml', 'iv_fluids',       30, 20, 'bags'),
('CLN002', 'Antidepressants SSRIs',  'medication',      40, 30, 'strips'),
('CLN002', 'Blood Glucose Strips',   'diagnostics',      5, 50, 'strips'),     -- LOW STOCK
('CLN003', 'Salbutamol Inhaler',     'medication',      12,  5, 'units'),
('CLN003', 'Spirometer Filters',     'diagnostics',      3, 10, 'units');      -- LOW STOCK

-- ── Follow-up Reminders ──────────────────────────────────────
INSERT INTO followup_reminders (patient_id, type, message, scheduled_at, status) VALUES
('P001', 'medication', 'Time to take your evening Metformin and Aspirin!', NOW() + INTERVAL '6 hours', 'pending'),
('P001', 'appointment', 'Your cardiology appointment is tomorrow at 9:00 AM with Dr. Priya Sharma.', NOW() + INTERVAL '20 hours', 'pending'),
('P002', 'medication', 'Remember to take Levothyroxine 30 minutes before breakfast tomorrow.', NOW() + INTERVAL '14 hours', 'pending'),
('P004', 'medication', 'Tonight is your weekly Methotrexate dose. Stay hydrated!', NOW() + INTERVAL '4 hours', 'pending'),
('P005', 'checkup', 'Monthly cardiac check-in: please log your current symptoms and send BP readings.', NOW() + INTERVAL '2 hours', 'pending');

-- ── Mental Health Screenings ─────────────────────────────────
INSERT INTO mental_health_screenings (patient_id, phq9_score, gad7_score, risk_level, coping_strategies, escalate) VALUES
('P001', 6, 5, 'low',      ARRAY['daily meditation 10 min','journaling','regular sleep schedule'], FALSE),
('P004', 12, 9, 'moderate', ARRAY['mindfulness app','CBT exercises','social support group','gentle yoga'], FALSE),
('P005', 15, 11, 'high',   ARRAY['professional counseling','breathing exercises','limit news consumption'], TRUE);

-- ── Wearable Data ────────────────────────────────────────────
INSERT INTO wearable_data (patient_id, device, heart_rate, steps, sleep_hours, spo2) VALUES
('P001', 'fitbit', 82, 6200, 6.5, 98.0),
('P001', 'fitbit', 88, 4500, 5.8, 97.5),
('P005', 'fitbit', 95, 1200, 5.0, 91.0),
('P005', 'fitbit', 98, 800,  4.5, 89.5),
('P003', 'apple_health', 85, 3000, 8.0, 96.0),
('P002', 'fitbit', 72, 7800, 7.0, 99.0);

-- ── Nutrition Logs ───────────────────────────────────────────
INSERT INTO nutrition_logs (patient_id, log_date, meals, calories, adherence, notes) VALUES
('P001', CURRENT_DATE - 1, '[{"meal":"breakfast","food":"oats + milk"},{"meal":"lunch","food":"grilled chicken salad"},{"meal":"dinner","food":"dal + 2 rotis"}]', 1750, TRUE,  'Good adherence today'),
('P001', CURRENT_DATE,     '[{"meal":"breakfast","food":"oats + milk"},{"meal":"lunch","food":"biryani (cheat)"}]', 2100, FALSE, 'Ate out for lunch — high calorie'),
('P005', CURRENT_DATE - 1, '[{"meal":"breakfast","food":"idli x4"},{"meal":"lunch","food":"brown rice + rasam"}]', 1500, TRUE,  'Good portions, low sodium');

-- ── Fitness Logs ─────────────────────────────────────────────
INSERT INTO fitness_logs (patient_id, log_date, activity, duration_minutes, calories_burned, notes) VALUES
('P001', CURRENT_DATE - 1, 'brisk walking', 30, 180, 'Morning walk at park'),
('P001', CURRENT_DATE - 2, 'yoga',          25, 120, 'Online yoga session'),
('P002', CURRENT_DATE - 1, 'walking',       20,  90, 'Evening stroll'),
('P005', CURRENT_DATE - 1, 'breathing exercises', 15, 40, 'Pursed lip breathing + diaphragmatic exercises');

-- ── Product Catalog ──────────────────────────────────────────
INSERT INTO product_catalog (name, category, partner, description, tags, price_inr) VALUES
('Omega-3 Fish Oil 1000mg',         'supplement', 'HealthVit',       'EPA + DHA for cardiac health',                       ARRAY['cardiac','cholesterol','heart'],               799),
('Vitamin D3 + K2 Drops',           'supplement', 'Healthkart',      'Bone health and immunity support',                   ARRAY['bones','immunity','vitamin_d'],                599),
('Magnesium Glycinate 400mg',        'supplement', 'NOW Foods India', 'Sleep quality and muscle relaxation',                ARRAY['sleep','stress','anxiety','muscle'],           999),
('CGM Continuous Glucose Monitor',  'device',     'Dexcom India',    '14-day real-time glucose tracking for diabetics',    ARRAY['diabetes','glucose','monitoring'],            4999),
('Spirometer for Home Use',         'device',     'Nidek Medical',   'Personal peak flow monitoring for COPD/Asthma',      ARRAY['copd','asthma','pulmonology','breathing'],    2499),
('Yoga Mat Premium',                'fitness',    'Decathlon India', 'Anti-slip 6mm yoga mat for home workouts',           ARRAY['fitness','yoga','stress'],                     899),
('Ayurvedic Arthritis Oil',         'supplement', 'Zandu',           'Joint pain relief oil with Ayurvedic formulation',   ARRAY['arthritis','joint_pain','orthopedics'],        349),
('Mental Wellness App - 1 Year',    'service',    'Wysa',            'AI + human therapist hybrid mental health support',  ARRAY['mental_health','anxiety','depression'],        2999),
('Diabetic Care Pack',              'supplement', 'HealthVit',       'Chromium, Alpha lipoic acid, Bitter melon extract',  ARRAY['diabetes','glucose','insulin_sensitivity'],    1299),
('HEPA Air Purifier For Bedroom',   'device',     'Dyson India',     'Removes allergens, pollutants — ideal for asthma',   ARRAY['asthma','allergy','pulmonology','air'],       18999);
