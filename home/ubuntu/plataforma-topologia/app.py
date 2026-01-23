from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessao'

# Configurações de Login
USUARIO_ADMIN = 'suporte'
SENHA_ADMIN = 'senha123'

# Caminhos
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
EXCEL_PATH = os.path.join(BASE_DIR, 'data', 'clientes.xlsx')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'imagens')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def carregar_dados():
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
        # Garante que as colunas existam
        colunas_esperadas = ['Cliente', 'Contrato', 'Topologia', 'Endereço', 'Data', 'Criada Por', 'Andamento']
        for col in colunas_esperadas:
            if col not in df.columns:
                df[col] = ""
        return df
    return pd.DataFrame(columns=['Cliente', 'Contrato', 'Topologia', 'Endereço', 'Data', 'Criada Por', 'Andamento'])

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
    # Adiciona um ID temporário para as rotas baseado no index se não houver ID real
    df['id_temp'] = df.index
    clientes = df.to_dict('records')
    return render_template('dashboard.html', clientes=clientes)

@app.route('/projeto/<int:id>')
def projeto(id):
    if 'logado' not in session:
        return redirect(url_for('login'))
    df = carregar_dados()
    if id >= len(df):
        flash('Projeto não encontrado!', 'warning')
        return redirect(url_for('dashboard'))
    
    cliente = df.iloc[id].to_dict()
    # Lógica para encontrar a imagem: usa o nome da coluna Topologia + .png se não tiver extensão
    img_name = str(cliente['Topologia'])
    if img_name and not any(img_name.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
        img_name += ".png"
    cliente['imagem_render'] = img_name
    
    return render_template('projeto.html', cliente=cliente)

@app.route('/adicionar', methods=['POST'])
def adicionar():
    if 'logado' not in session:
        return redirect(url_for('login'))
    
    nova_linha = {
        'Cliente': request.form.get('Cliente'),
        'Contrato': request.form.get('Contrato'),
        'Topologia': request.form.get('Topologia'),
        'Endereço': request.form.get('Endereço'),
        'Data': request.form.get('Data'),
        'Criada Por': request.form.get('Criada Por'),
        'Andamento': request.form.get('Andamento')
    }
    
    file = request.files.get('imagem')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Se enviou imagem, podemos salvar o nome dela na coluna Topologia ou manter o nome do campo
    
    df = carregar_dados()
    df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)
    salvar_dados(df)
    flash('Cliente adicionado com sucesso!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/excluir/<int:id>')
def excluir(id):
    if 'logado' not in session:
        return redirect(url_for('login'))
    df = carregar_dados()
    df = df.drop(df.index[id])
    salvar_dados(df)
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)