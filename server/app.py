from flask import Flask, request, render_template, redirect, url_for, session, flash
from pymongo import MongoClient, ReturnDocument
from werkzeug.security import generate_password_hash, check_password_hash
import util
from datetime import datetime
from functools import wraps
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='client/templates', static_folder='client/static')
app.secret_key = 'your-secret-key-here'  # Required for sessions

# MongoDB setup
client = MongoClient(os.getenv('MONGO_URI'))
db = client['cancer_db']
records = db['risk_records']
users = db['users']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_next_sequence(name: str) -> int:
    counter = db.counters.find_one_and_update(
        {'_id': name},
        {'$inc': {'seq': 1}},
        return_document=ReturnDocument.AFTER,
        upsert=True
    )
    return counter['seq']

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if users.find_one({'username': username}):
            flash('Username already exists')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        users.insert_one({
            'username': username,
            'password': hashed_password
        })
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = users.find_one({'username': username})
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            return redirect(url_for('home'))
        
        flash('Invalid username or password')
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('app.html', username=session.get('username'))

@app.route('/predict_risk', methods=['POST'])
@login_required
def predict_risk():
    try:
        db_no = get_next_sequence('risk_records')
        patient = {
            'db_no': db_no,
            'user_id': session['user_id'],
            'username': session['username'],
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'height': float(request.form['height']),
            'weight': float(request.form['weight']),
            'alcohol_consumption': float(request.form['alcohol_consumption']),
            'smoking': int(request.form['smoking']),
            'genetic_risk': int(request.form['genetic_risk']),
            'physical_activity': float(request.form['physical_activity']),
            'diabetes': int(request.form['diabetes']),
            'hypertension': int(request.form['hypertension']),
            'timestamp': datetime.utcnow()
        }
    except Exception:
        return util.apology("Invalid input values", 400)

    patient['risk_percentage'] = util.predict_risk(
        patient['age'], patient['sex'],
        patient['weight'], patient['height'],
        patient['alcohol_consumption'], patient['smoking'],
        patient['genetic_risk'], patient['physical_activity'],
        patient['diabetes'], patient['hypertension']
    )

    records.insert_one(patient)
    return render_template('risk.html', patient=patient)

@app.route('/history')
@login_required
def history():
    user_records = list(records.find({'user_id': session['user_id']}).sort('db_no', -1))
    return render_template('history.html', records=user_records)

@app.route('/delete/<int:db_no>', methods=['POST'])
@login_required
def delete_record(db_no):
    result = records.delete_one({'db_no': db_no, 'user_id': session['user_id']})
    if result.deleted_count == 0:
        return util.apology(f"No record with Record No {db_no}", 404)
    return redirect(url_for('history'))

@app.errorhandler(404)
def page_not_found(e):
    return util.apology("Page not found", 404)

if __name__ == '__main__':
    app.run(debug=True) 