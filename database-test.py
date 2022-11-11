import pyrebase

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

# ----- works ------#
# data = {"name" : "Test", "address" : "Test","email":"test","Donor":"test","Distributor":"test"}
# db.push(data)
# ---- for updating data ---#
# data_file = db.get()
# for details in data_file.each():
#   print(details.key())
#   db.child(details.key()).update({"name":"bro"})
#----- for updating category ------#
#
# data_file = db.child("Data").get()
# for details in data_file.each():
# print(details.key())
#   print(details.val())
# for pushing data
# data = {"Donor name": "Test", "Location": "Test", "Contact details": "Test",
#         "Food details": "Test", "Donor mail": "Test", "Distributor mail": "Test"}
# db.child("Data").child("check").update(data)

# data = {'email': ['check1', 'check2', 'check3']}
# print(list(db.child("Aadhar").get().val().values()))
# email = 'user1@gmail.com'
# print(db.child("Data").child(email.split(
#     '@')[0]).child("Username").get().val())
# email = "user1@gmail.com"
# password = "password"

# auth.sign_in_with_email_and_password(email, password)

# db.child("Data").child("-Mwg6KdEDE3GC9ysKqb0").update({"email":"Test"})

# data_file = db.child("Data").get()
# for details in data_file.each():
#   print(details.key())
#   if details.key() == "Mwg6KdEDE3GC9ysKqb0":
#     db.child("Data").child(details.key()).child("email").update("Test")


# data = {"vehicle_name": "Swift Desire", "seats": 4, "quantity": 5, "pkm": 12}
# db.child("Vehicles").push(data)

# db.child("Users").push('user1')

# print(list(db.child("Admin Mail").get().val()))


# db.child("Vehicles").child(
#     '-NGYDTZzYfEe1E0Y3_iF').update({"quantity": 10})
email = 'user1@gmail.com'
print(db.child("Data").child(email.split(
    '@')[0]).child("bookings").get().val())
