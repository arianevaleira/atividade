@app.route('/novoexercicio', methods=['GET', 'POST'])
@login_required
def novo_exercicio():
    if request.method == 'POST':
        nome_ex = request.form['nome_exercicio']
        descricao_ex = request.form['descricao_exercicio']


        conn = obter_conexao()  
        cursor = conn.cursor()      
        cursor.execute("INSERT INTO exercicios(nome_ex, descricao) VALUES (?,?)", (nome_ex, descricao_ex))
        conn.commit()
        conn.close()

        flash('exercicio adicionado com sucesso!', 'success')
        return redirect(url_for('listarexercicios'))

    else:
        return render_template('novo_exercicio.html')

@app.route('/listarexercicios', methods=['POST', 'GET'])
def listarexercicios():
    conn = obter_conexao()  
    cursor = conn.cursor()      
    exercicios = cursor.execute("SELECT * FROM exercicios").fetchall()
    conn.close()
    return render_template("listarexercicios.html", exercicios=exercicios)
    
# 5 - bloquear uma rota
@app.route('/dashboard')
@login_required
def dash():
    return render_template('pages/dash.html')

# 8 - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


# 7 - logar um usuário já existente
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        matricula = request.form['matricula']
        password = request.form['password']   
        user = User.get_by_matricula(matricula)
        if check_password_hash(user['password'], password):
            login_user(User.get(user['id']))
            flash("Você está logado")
            return redirect(url_for('dash'))
        else:
            return redirect(url_for('login'))
    return render_template('pages/auth/login.html')


{% extends 'layout.html' %} {% block conteudo %}
exercicios cadastrados:
{% for ex in exercicios %}
         {{ex['nome_ex']}} | {{ex['descricao']}}
{% endfor %}
{% endblock %}


