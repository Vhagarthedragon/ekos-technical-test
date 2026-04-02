INSERT INTO knowledge_articles (title, content, category, tags) VALUES

('How to submit an insurance claim',
'To submit an insurance claim: go to Billing > New Claim, select the patient and visit date, enter CPT and ICD-10 codes, verify insurance info, then click Submit. Claims are typically processed within 30 days. For rejections, check the reason under Billing > Claims > Rejected and resubmit with corrections.',
'billing', ARRAY['insurance', 'claims', 'CPT', 'ICD-10']),

('Understanding your EOB',
'An Explanation of Benefits (EOB) shows what was billed, what insurance paid, adjustments, and patient responsibility. EOBs are auto-imported when you connect your clearinghouse. Go to Billing > EOBs to view and post payments. Denial reason codes explain why a claim was rejected.',
'billing', ARRAY['EOB', 'insurance', 'payments', 'denial']),

('Setting up patient payment plans',
'Go to Patient Profile > Billing > Add Payment Plan. Set the total, number of installments, and due dates. ClinicDesk sends automatic reminders 3 days before each due date and supports card-on-file for auto-charges. Plans can be paused or modified anytime.',
'billing', ARRAY['payment plan', 'collections']),

('Scheduling a new patient',
'Click + on the calendar or press N, select New Patient, enter their contact info, choose provider and appointment type, pick a time slot, and choose whether to send a confirmation. New patients automatically receive intake forms by email.',
'scheduling', ARRAY['appointment', 'new patient', 'calendar']),

('Handling cancellations and no-shows',
'To cancel: open the appointment and click Cancel. For no-shows, mark as No Show to update the patient record and trigger a follow-up message. Patients with 3+ no-shows can be flagged to require prepayment. Configure thresholds under Settings > Scheduling > No-Show Policy.',
'scheduling', ARRAY['cancellation', 'no-show', 'waitlist']),

('Verifying insurance eligibility',
'Open the patient record, go to the Insurance tab, and click Verify Eligibility. ClinicDesk checks active coverage, deductibles, copays, and remaining benefits in real time. You can also run batch verification for all patients scheduled in the next 7 days from Billing > Batch Eligibility.',
'insurance', ARRAY['eligibility', 'verification', 'deductible']),

('Coordinating secondary insurance',
'Add both plans under Patient Profile > Insurance. When billing, ClinicDesk handles COB automatically: it submits to primary first, then creates a secondary claim with the primary payment details. Make sure relationship and group numbers are correct for both plans.',
'insurance', ARRAY['secondary insurance', 'COB']),

('Resetting your password',
'Click Forgot Password on the login screen and enter your email. The reset link is valid for 24 hours. Admins can reset staff passwords from Settings > Users > [user] > Reset Password. Passwords must be at least 12 characters and include numbers and symbols.',
'general', ARRAY['password', 'login', 'security']),

('Upgrading your subscription',
'Go to Settings > Billing > Subscription. Plans: Starter (1 provider), Growth (up to 5 providers, billing + insurance), Enterprise (unlimited providers, all features, priority support). Upgrades are immediate and prorated. Contact sales@clinicdesk.com for Enterprise pricing or add-ons.',
'general', ARRAY['upgrade', 'subscription', 'pricing']),

('Exporting data and reports',
'Go to Reports > Export to download patient demographics, appointment history, billing summaries, or insurance reports as CSV, Excel, or PDF. For HIPAA-compliant bulk exports, contact support. Scheduled reports can be emailed automatically to designated staff.',
'general', ARRAY['export', 'reports', 'data', 'HIPAA']);
