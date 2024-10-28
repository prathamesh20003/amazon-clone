import firebase_admin
from flask import Flask, render_template, request, redirect, url_for, flash, session
from firebase_admin import credentials, firestore, auth

firebaseConfig ={
    #paste firebase database config from project settings
}

# Initialize Firebase Admin with service account
cred = credentials.Certificate("") #add file path of firebase sdk json file 
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Add a secret key for session management

@app.route('/')
def home():
    email = session.get('email')  # Check if user is logged in and get email from session
    username = session.get('username')
    return render_template('index.html', username=username)  # Pass email to template

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

@app.route('/userform')
def userform():
    return render_template('UserForm.html')

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

        # Retrieve user information from Firestore
        user_ref = db.collection("users").document(user.uid)
        user_doc = user_ref.get()

        if user_doc.exists:
            # Get the username from Firestore
            username = user_doc.to_dict().get("username")

            # Store email and username in session after login
            session['user_id'] = user.uid
            session['email'] = user.email  # Store email in session
            session['username'] = username  # Store username in session
        
            return redirect(url_for("home"))
        else:
            flash('User not found', 'error')
            return redirect(url_for("SignIn"))
    
    except Exception as e:
        flash('Login failed: {}'.format(str(e)), 'error')
        return redirect(url_for("SignIn"))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('home'))  # Redirect if not logged in
    email = session.get('email')  # Get the logged-in user's email from session
    return f'Welcome, {email}! <a href="/logout">Logout</a>'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
