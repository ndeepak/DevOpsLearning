from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'thisissecret'  # Insecure key

# Simulated user database
users = {
    'alice': {'password': 'alice123', 'id': 101, 'role': 'user'},
    'bob':   {'password': 'bob123', 'id': 102, 'role': 'user'},
    'admin': {'password': 'admin123', 'id': 1,   'role': 'admin'},
}

@app.route('/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! <a href='/logout'>Logout</a><br><a href='/profile?id={users[session['username']]['id']}'>My Profile</a><br><a href='/admin'>Admin Page</a>"
    return '''
        <form method="POST" action="/login">
            Username: <input name="username"><br>
            Password: <input type="password" name="password"><br>
            <button type="submit">Login</button>
        </form>
    '''

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = users.get(username)
    if user and user['password'] == password:
        session['username'] = username
        session['role'] = user['role']
        return redirect(url_for('home'))
    return 'Login Failed'

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    target_id = request.args.get('id')
    for username, data in users.items():
        if str(data['id']) == target_id:
            return f"Profile of {username}<br>User ID: {data['id']}<br>Role: {data['role']}"
    return "Profile not found"

@app.route('/admin')
def admin():
    if session.get('role') == 'admin':
        return "Welcome Admin! You have full control."
    return "Access Denied"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
# To run this Flask application, save the code in a file named app.py and run it using:
# python app.py