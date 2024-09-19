from flask import Flask, session, request, render_template, url_for, redirect
from flask_login import LoginManager
from models import Users, conexao  # Certifique-se de importar o que precisar

app = Flask(__name__)

login_manager = LoginManager()  # Inicializa o LoginManager
login_manager.init_app(app)

# Chave para criptografia de cookies na sessão
app.config['SECRET_KEY'] = 'superdificil'

# Função usada pelo LoginManager para carregar dados do usuário logado
@login_manager.user_loader
def load_user(user_id):
    return Users.get(user_id)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dash():
    if 'user' not in session:  # Se user não tiver uma sessão
        return redirect(url_for('index'))
    return render_template('dashboard.html', email=session['user'])  # Cria uma sessão chamada user

@app.route('/login', methods=['POST', 'GET'])
def login():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('login.html')
    else:
        matricula = request.form.get('matricula')
        email = request.form.get('email')
        senha = request.form.get('senha')

        user = Users.get_by_email(email)
        if user and user.senha == senha:
            session['user'] = email
            return redirect(url_for('dash'))
        else:
            return "Email ou senha incorretos"

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user' in session:
        return redirect(url_for('dash'))

    if request.method == 'GET':
        return render_template('register.html')
    else:
        matricula = request.form['matricula']
        email = request.form['email']
        senha = request.form['senha']

        user = Users.get_by_email(email)  # Verifica se o email já está registrado
        if user:
            return redirect(url_for('login'))

        conn = conexao()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO tb_usuarios (usu_mat, usu_email, usu_senha) VALUES (?, ?, ?)', (matricula, email, senha))
        conn.commit()
        conn.close()

        session['user'] = email
        return redirect(url_for('dash'))


@app.route('/cadastrar_exercicio', methods=['GET', 'POST'])
def cadastrar_exercicio():
    if request.method == 'GET':
        return render_template('cadastrar.html')
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        matricula = request.form['matricula']  # Recebe a matrícula do usuário logado

        conn = conexao()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO tb_exercicios (exe_nome, exe_descricao, exe_usu_mat) VALUES (?, ?, ?)',
            (nome, descricao, matricula)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('dash'))  

@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)