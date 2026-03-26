import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

fake = Faker()
Faker.seed(42)
np.random.seed(42)

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(base_path, 'data')

# Ensure data directory exists
os.makedirs(data_dir, exist_ok=True)

# Generate Patients
def generate_patients(n=1000):
    print("Generating patients...")
    patients = []
    cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose']
    
    for i in range(1, n+1):
        patients.append({
            'patient_id': f'P{i:05d}',
            'age': random.randint(1, 90),
            'gender': random.choice(['Male', 'Female']),
            'city': random.choice(cities),
            'registration_date': fake.date_between(start_date='-2y', end_date='today')
        })
    df = pd.DataFrame(patients)
    df.to_csv(os.path.join(data_dir, 'patients.csv'), index=False)
    return df

# Generate Appointments
def generate_appointments(patients_df, n=3000):
    print("Generating appointments...")
    appointments = []
    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'General Medicine', 'Gynecology']
    
    for i in range(1, n+1):
        patient_id = random.choice(patients_df['patient_id'])
        dept = random.choice(departments)
        
        # Determine if it's a no-show
        is_no_show = random.choices([True, False], weights=[0.2, 0.8])[0]
        
        # Afternoon appointments have slightly higher no-show
        fake_date = fake.date_time_between(start_date='-1y', end_date='now')
        hour = fake_date.hour
        if 14 <= hour <= 18:
            is_no_show = random.choices([True, False], weights=[0.3, 0.7])[0]
            
        sms = random.choices(['Yes', 'No'], weights=[0.7, 0.3])[0]
        if sms == 'Yes':
            is_no_show = random.choices([True, False], weights=[0.1, 0.9])[0] # sms reduces no-show
            
        appointments.append({
            'appointment_id': f'A{i:05d}',
            'patient_id': patient_id,
            'department': dept,
            'appointment_date': fake_date.strftime('%Y-%m-%d'),
            'appointment_time': fake_date.strftime('%H:%M:%S'),
            'sms_reminder': sms,
            'previous_no_shows': random.randint(0, 3) if random.random() < 0.2 else 0,
            'status': 'No-show' if is_no_show else 'Show'
        })
    df = pd.DataFrame(appointments)
    df.to_csv(os.path.join(data_dir, 'appointments.csv'), index=False)
    return df

# Generate Visits
def generate_visits(appointments_df):
    print("Generating visits from attended appointments...")
    visits = []
    # Only those who showed up
    shows = appointments_df[appointments_df['status'] == 'Show'].copy()
    
    doctors = [f'D{i:03d}' for i in range(1, 21)]
    
    for i, row in shows.iterrows():
        # Parse appointment time
        appt_datetime_str = f"{row['appointment_date']} {row['appointment_time']}"
        appt_datetime = datetime.strptime(appt_datetime_str, '%Y-%m-%d %H:%M:%S')
        
        # Admission time is roughly around appointment time
        admission_time = appt_datetime - timedelta(minutes=random.randint(0, 30))
        
        # Base waiting time
        wait_mins = random.randint(10, 60)
        
        # Peak hours have longer wait times (4PM - 7PM)
        if 16 <= appt_datetime.hour <= 19:
            wait_mins += random.randint(20, 60)
            
        consultation_time = admission_time + timedelta(minutes=wait_mins)
        discharge_time = consultation_time + timedelta(minutes=random.randint(15, 45))
        
        visits.append({
            'visit_id': f'V{len(visits)+1:05d}',
            'patient_id': row['patient_id'],
            'department': row['department'],
            'admission_time': admission_time.strftime('%Y-%m-%d %H:%M:%S'),
            'consultation_time': consultation_time.strftime('%Y-%m-%d %H:%M:%S'),
            'discharge_time': discharge_time.strftime('%Y-%m-%d %H:%M:%S'),
            'waiting_time': wait_mins,
            'doctor_id': random.choice(doctors),
            'bed_assigned': random.choices(['Yes', 'No'], weights=[0.1, 0.9])[0],
            'visit_type': 'OPD' # Assuming mostly OPD from appointments
        })
        
    df = pd.DataFrame(visits)
    df.to_csv(os.path.join(data_dir, 'visits.csv'), index=False)
    return df

if __name__ == '__main__':
    print("Starting data generation...")
    p_df = generate_patients(2000)
    a_df = generate_appointments(p_df, 5000)
    v_df = generate_visits(a_df)
    print("Data generation complete! Files saved in 'data/' directory.")
