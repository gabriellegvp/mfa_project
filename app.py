from flask import Flask, render_template, request, redirect, url_for, session
import pyotp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Gera uma chave secreta única para a sessão

# Secret Key para o TOTP
SECRET_KEY = pyotp.random_base32()  # Gera uma chave secreta única
totp = pyotp.TOTP(SECRET_KEY)

@app.route('/')
def index():
    if 'authenticated' in session:
        return f"<h1>Bem-vindo, {session['username']}! Você está autenticado.</h1><a href='/logout'>Logout</a>"
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    # Verifica o usuário e senha (pode ser integrado com um banco de dados)
    if username == "admin" and password == "senha_forte":
        session['username'] = username
        return redirect(url_for('verify_otp'))
    return "<h3>Login falhou! Usuário ou senha incorretos.</h3>"

@app.route('/verify_otp')
def verify_otp():
    return render_template('verify_otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form['otp']
    if totp.verify(otp):  # Valida o código TOTP
        session['authenticated'] = True
        return redirect(url_for('index'))
    return "<h3>Código incorreto! Tente novamente.</h3>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
