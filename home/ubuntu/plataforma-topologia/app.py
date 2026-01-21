from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

# Configurações de Login
USUARIO_ADMIN = 'suporte'
SENHA_ADMIN = 'senha123'

# Caminhos baseados no diretório do arquivo para evitar erros em diferentes sistemas
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'clientes.xlsx')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'imagens')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def carregar_dados():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    return pd.DataFrame(columns=['id', 'nome_cliente', 'titulo_sistema', 'imagem', 'resumo'])

def salvar_dados(df):
    df.to_excel(EXCEL_PATH, index=False)

@app.route('/')
def index():
    if 'logado' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')
        if usuario == USUARIO_ADMIN and senha == SENHA_ADMIN:
            session['logado'] = True
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha incorretos!', 'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'logado' not in session:
        return redirect(url_for('login'))
    df = carregar_dados()
    clientes = df.to_dict('records')
    return render_template('dashboard.html', clientes=clientes)

@app.route('/projeto/<int:id>')
def projeto(id):
    if 'logado' not in session:
        return redirect(url_for('login'))
    df = carregar_dados()
    cliente = df[df['id'] == id].to_dict('records')
    if not cliente:
        flash('Projeto não encontrado!', 'warning')
        return redirect(url_for('dashboard'))
    return render_template('projeto.html', cliente=cliente[0])

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'logado' not in session:
        return redirect(url_for('login'))
    
    nome = request.form.get('nome_cliente')
    titulo = request.form.get('titulo_sistema')
    resumo = request.form.get('resumo')
    file = request.files.get('imagem')
    
    filename = 'default.png'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    df = carregar_dados()
    novo_id = int(df['id'].max() + 1) if not df.empty else 1
    
    nova_linha = {
        'id': novo_id,
        'nome_cliente': nome,
        'titulo_sistema': titulo,
        'imagem': filename,
        'resumo': resumo
    }
    
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    salvar_dados(df)
    flash('Cliente adicionado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    if 'logado' not in session:
        return redirect(url_for('login'))
    
    df = carregar_dados()
    idx = df[df['id'] == id].index
    
    if not idx.empty:
        df.at[idx[0], 'nome_cliente'] = request.form.get('nome_cliente')
        df.at[idx[0], 'titulo_sistema'] = request.form.get('titulo_sistema')
        df.at[idx[0], 'resumo'] = request.form.get('resumo')
        
        file = request.files.get('imagem')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            df.at[idx[0], 'imagem'] = filename
            
        salvar_dados(df)
        flash('Projeto atualizado com sucesso!', 'success')
    
    return redirect(url_for('dashboard'))

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'logado' not in session:
        return redirect(url_for('login'))
    
    df = carregar_dados()
    df = df[df['id'] != id]
    salvar_dados(df)
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    # Porta dinâmica para compatibilidade com serviços de nuvem
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
