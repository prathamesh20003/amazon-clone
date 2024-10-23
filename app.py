import firebase_admin
from flask import Flask, render_template, request, redirect, url_for, flash, session
from firebase_admin import credentials, firestore, auth

firebaseConfig = {
    'apiKey': "AIzaSyC_-alE4HXmS7kG1E4zi3Bsud8t--KaXZc",
    'authDomain': "clone-rospl-project.firebaseapp.com",
    'projectId': "clone-rospl-project",
    'storageBucket': "clone-rospl-project.appspot.com",
    'messagingSenderId': "250595430287",
    'appId': "1:250595430287:web:6a6eb16d544272ea8585fa"
}

# Initialize Firebase Admin with service account
cred = credentials.Certificate("D:\\downloads\\vscode\\rospl\\amazon-clone\\firebaseadmin.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Add a secret key for session management

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/SignIn')
def SignIn():
    return render_template('SignIn.html')

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
        # Create user with Firebase Admin SDK
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

        return redirect(url_for("SignIn"))

    except Exception as e:
        return f"An error occurred: {e}", 400

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Firebase Admin SDK does not support password verification directly
        # You may need to handle login on the client-side or use Firebase Authentication REST API
        user = auth.get_user_by_email(email)

        # Store user in session (you can store user UID or other info)
        session['user_id'] = user.uid
        
        return redirect(url_for("dashboard"))
    
    except Exception as e:
        flash('Login failed: {}'.format(str(e)), 'error')
        return redirect(url_for("SignIn"))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in
    return f'Welcome, {session["user_id"]}! <a href="/logout">Logout</a>'

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user from session
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
