from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/billing')
def billing():
    return render_template('billing.html')

@app.route('/product')
def product():
    return render_template('product.html')

if __name__ == '__main__':
    app.run()