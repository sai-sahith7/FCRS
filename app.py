from flask import Flask, render_template, request, redirect, url_for, session
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY'] = "c6e803cd18a8c528c161eb9fcf013245248506ffb540ff70"
firebaseConfig = {'apiKey': "AIzaSyAAgnH-E3lVhXdusCGamTAwfpB8nIh_rJw",
                  'authDomain': "fcrs-26b41.firebaseapp.com",
                  'projectId': "fcrs-26b41",
                  'storageBucket': "fcrs-26b41.appspot.com",
                  'messagingSenderId': "595206851375",
                  'appId': "1:939176945790:web:78681964fa92d0cde8102f",
                  'measurementId': "G-6ZNFZM4916",
                  'databaseURL': "https://fcrs-26b41-default-rtdb.asia-southeast1.firebasedatabase.app/"
                  }
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


@app.route('/')
def index():
    if session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('email', None)
    session.pop('uname', None)
    session.pop('admin', None)
    return redirect(url_for('index'))


@app.route('/home')
def home():
    if session.get('logged_in'):
        return render_template('home.html')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error_msg = ""
    if request.method == 'POST':
        email = str(request.form['email'])
        password = str(request.form['password'])
        try:
            auth.sign_in_with_email_and_password(email, password)
            session['email'] = email
            session['logged_in'] = True
            session['uname'] = str(db.child("Data").child(
                email.split('@')[0]).child("Username").get().val())
            if email in list(db.child("Admin Mail").get().val()):
                session['admin'] = True
                return redirect(url_for('admin'))
            session['admin'] = False
            return redirect(url_for('home'))
        except:
            error_msg = "Invalid Credentials. Try Again."
    if session.get('logged_in'):
        return redirect(url_for('home'))
    return render_template('login.html', error_msg=error_msg)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error_msg = ""
    if request.method == 'POST':
        username = str(request.form['username'])
        email = str(request.form['email'])
        password = str(request.form['password'])
        confirm_pass = str(request.form['confirm-pass'])
        dob = str(request.form['dob'])
        dl = str(request.form['dl'])
        aadhaar = int(request.form['aadhaar'])
        date, month, year = int(request.form['date']), int(
            request.form['month']), int(request.form['year'])
        print(date, month, year)
        if email.count('@') != 1:
            error_msg = "Invalid Email. Try Again."
        elif password != confirm_pass:
            error_msg = "Passwords do not match. Try Again."
        elif int(dob.split('-')[0]) > year-18:
            error_msg = "You must be 18 years or older to register."
        elif int(dob.split('-')[0]) == year-18:
            if int(dob.split('-')[1]) > month:
                error_msg = "You must be 18 years or older to register."
            elif int(dob.split('-')[1]) == month:
                if int(dob.split('-')[2]) > date:
                    error_msg = "You must be 18 years or older to register."
        elif len(dl) != 15 or (dl[:2].isalpha() is False) or (dl[2:].isdigit() is False):
            error_msg = "Invalid Driving License Number. Try Again."
        elif len(str(aadhaar)) != 12:
            error_msg = "Invalid Aadhaar Number. Try Again."
        elif aadhaar in list(db.child("Aadhaar").get().val().values()):
            error_msg = "Aadhaar Number already registered. Try Again."
        elif dl in list(db.child("DL").get().val().values()):
            error_msg = "Driving License Number already registered. Try Again."
        if error_msg == "":
            try:
                auth.create_user_with_email_and_password(email, password)
                db.child("Aadhaar").push(aadhaar)
                db.child("DL").push(dl)
                data = {"Username": username, "DOB": dob, "Email": email,
                        "Aadhaar": aadhaar, "DL": dl, "km": 0, "pending": 0, "bookings": 0}
                db.child("Data").child(email.split('@')[0]).update(data)
                db.child("Users").push(username)
                session['email'] = email
                session['logged_in'] = True
                session['admin'] = False
                session['uname'] = username
                return redirect(url_for('home'))
            except:
                error_msg = "Email already registered. Try Again."
    return render_template('signup.html', error_msg=error_msg)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('logged_in'):
        if session.get('admin'):
            if request.method == 'POST':
                vehicle_name = str(request.form['name'])
                pkm = int(request.form['pkm'])
                seats = int(request.form['seats'])
                quantity = int(request.form['quantity'])
                vehicle_id = str(request.form['vehicle_id'])
                data = {'vehicle_name': vehicle_name, 'pkm': pkm,
                        'seats': seats, 'quantity': quantity}
                if vehicle_id == 'None':
                    db.child("Vehicles").push(data)
                else:
                    print(vehicle_id)
                    db.child("Vehicles").child(vehicle_id).update(data)
                return redirect(url_for('admin'))
            customers = get_customer_list()
            vehicles = get_vehicle_info()
            return render_template('admin index.html', customers=customers, vehicles=vehicles)
        return redirect(url_for('home'))
    return redirect(url_for('index'))


@app.route('/booking-details', methods=['GET', 'POST'])
def booking_details():
    error_msg = ""
    if request.method == 'POST':
        date = str(request.form['date'])
        hour = str(request.form['hour'])
        minute = str(request.form['minute'])
        pickup = str(request.form['from'])
        ampm = str(request.form['AMPM'])
        drop = str(request.form['to'])
        current_date = int(request.form['date1'])
        current_month = int(request.form['month'])
        current_year = int(request.form['year'])
        if int(date.split('-')[0]) < current_year:
            error_msg = "Invalid Date. Try Again."
        elif int(date.split('-')[0]) == current_year:
            if int(date.split('-')[1]) < current_month:
                error_msg = "Invalid Date. Try Again."
            elif int(date.split('-')[1]) == current_month:
                if int(date.split('-')[2]) < current_date:
                    error_msg = "Invalid Date. Try Again."
        if error_msg == "":
            data = {"Date": date, "Time": hour+':'+minute+' '+ampm,
                    "Pickup": pickup, "Drop": drop}
            vehicles = get_vehicle_info()
            return render_template('vehicle selection.html', booking_details=data, vehicles=vehicles)
        else:
            return render_template('home.html', error_msg=error_msg)

    return redirect(url_for('home'))


@app.route('/vehicle-selection', methods=['GET', 'POST'])
def vehicle_selection():
    if request.method == 'POST':
        vehicle_id = str(request.form['vehicle_id'])
        date = str(request.form['date'])
        time = str(request.form['time'])
        pickup = str(request.form['pickup'])
        drop = str(request.form['drop'])
        vehicle_name = str(request.form['vehicle_name'])
        print('vehicle_id', vehicle_id)
        # quant = db.child("Vehicles").child(
        #     vehicle_id).child("quantity").get().val()
        # db.child("Vehicles").child(vehicle_id).update(
        #     {"quantity": quant-1})
        data = {"Date": date, "Time": time, 'email': session['email'], "Pickup": pickup, 'name': session['uname'],
                "Drop": drop, "Vehicle": vehicle_id, "Status": "Booked", 'vehicle_name': vehicle_name, "Amount to be paid": 0}
        # db.child("Data").child(session['email'].split(
        #     '@')[0]).update({"bookings": db.child("Data").child(session['email'].split('@')[0]).child("bookings").get().val()+1})
        db.child("Bookings").push(data)
        return redirect(url_for('booking_history'))
    return redirect(url_for('home'))


@app.route('/booking-history', methods=['GET', 'POST'])
def booking_history():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    bookings = get_personal_bookings(session['email'])
    customers = get_customer_list()
    bookings_count = db.child("Data").child(
        session['email'].split('@')[0]).child("bookings").get().val()
    kms_count = db.child("Data").child(
        session['email'].split('@')[0]).child("km").get().val()
    pending_payment = db.child("Data").child(
        session['email'].split('@')[0]).child("pending").get().val()
    return render_template('booking history.html', bookings=bookings, customers=customers, bookings_count=bookings_count, kms_count=kms_count, pending_payment=pending_payment)


def get_personal_bookings(mail):
    bookings = db.child("Bookings").get().val()
    bookings_list = []
    if bookings is not None:
        for booking in bookings:
            if bookings[booking]['email'] == mail:
                bookings_list.append(bookings[booking])
    return bookings_list


def get_customer_list():
    customers = db.child("Users").get().val()
    customer_list = []
    if customers is not None:
        for customer in customers:
            customer_list.append(customers[customer])
    return customer_list


def get_vehicle_info():
    vehicles = db.child("Vehicles").get().val()
    vehicle_list = []
    if vehicles is not None:
        for vehicle in vehicles:
            temp = dict(vehicles[vehicle])
            temp['vehicle_id'] = vehicle
            print(temp)
            vehicle_list.append(temp)
    return vehicle_list


if __name__ == '__main__':
    app.run(debug=True)
