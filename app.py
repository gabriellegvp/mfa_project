from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyotp
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para proteger sessões

# Carregar a chave secreta do ambiente ou gerar uma nova
SECRET_KEY = os.environ.get("TOTP_SECRET", pyotp.random_base32())
totp = pyotp.TOTP(SECRET_KEY)

# Usuário e senha fictícios (para produção, use um banco de dados seguro)
USER_CREDENTIALS = {"admin": "senha_forte"}

@app.route('/')
def index():
    if 'authenticated' in session:
        return render_template('welcome.html', username=session['username'])
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    # Validação de credenciais
    if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
        session['username'] = username
        return redirect(url_for('verify_otp'))
    
    flash("Usuário ou senha incorretos. Tente novamente!", "error")
    return redirect(url_for('index'))

@app.route('/verify_otp')
def verify_otp():
    if 'username' not in session:
        flash("Faça login primeiro.", "error")
        return redirect(url_for('index'))
    return render_template('verify_otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    if 'username' not in session:
        flash("Sessão expirada. Faça login novamente.", "error")
        return redirect(url_for('index'))
    
    otp = request.form['otp']
    if totp.verify(otp):
        session['authenticated'] = True
        return redirect(url_for('index'))
    
    flash("Código OTP incorreto. Tente novamente!", "error")
    return redirect(url_for('verify_otp'))

@app.route('/logout')
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
