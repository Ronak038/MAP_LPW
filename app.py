from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient, Doctor, Appointment
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

db.init_app(app)

@app.before_first_request
def create_tables():

    db.create_all()

@app.route('/patients')
def view_patients():
    patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        contact = request.form['contact']

        new_patient = Patient(name=name, age=age, gender=gender, contact=contact)
        db.session.add(new_patient)
        db.session.commit()
        
        return redirect(url_for('view_patients'))
    
    return render_template('add_patient.html')


@app.route('/doctors')
def view_doctors():
    doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
def add_doctor():
    if request.method == 'POST':
        name = request.form['name']
        specialization = request.form['specialization']
        contact = request.form['contact']

        new_doctor = Doctor(name=name, specialization=specialization, contact=contact)
        db.session.add(new_doctor)
        db.session.commit()

        return redirect(url_for('view_doctors'))
    
    return render_template('add_doctor.html')


@app.route('/appointments', methods=['GET', 'POST'])
def appointments():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        reason = request.form['reason']
        

        appointment_date = datetime.strptime(date, '%Y-%m-%d %H:%M')

        new_appointment = Appointment(patient_id=patient_id, doctor_id=doctor_id, date=appointment_date, reason=reason)
        db.session.add(new_appointment)
        db.session.commit()

        return redirect(url_for('view_appointments'))
    
    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointments.html', patients=patients, doctors=doctors)


@app.route('/appointments/view')
def view_appointments():
    appointments = Appointment.query.all()
    return render_template('view_appointments.html', appointments=appointments)

if __name__ == '__main__':
    app.run(debug=True)
