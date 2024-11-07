import firebase_admin
from flask import Flask,render_template, request, redirect, url_for
from firebase_admin import credentials, firestore, auth

firebaseConfig ={
    #enter sdk config ftom firebase
}
# Initialize Firebase Admin with service account
cred = credentials.Certificate("firebase admin sdk location")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/SignUp')
def SignUp():
    return render_template('SignUp.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/product')
def product():
    return render_template('product.html')

@app.route("/register", methods=["POST"])
def register():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    location = request.form.get("location")

    if password != confirm_password:
        return "Passwords do not match", 400

    try:
        # Create user with Firebase Authentication
        user = auth.create_user(
            email=email,
            password=password,
            display_name=username
        )

        # Store additional user data in Firestore
        db.collection("users").document(user.uid).set({
            "username": username,
            "email": email,
            "location": location
        })

        return redirect(url_for("login"))

    except Exception as e:
        return f"An error occurred: {e}", 400


if __name__ == '__main__':
    app.run()