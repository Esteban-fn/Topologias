# Guia de Instalação - Windows 11

Siga estes passos para rodar o projeto localmente no seu computador.

## 1. Instalar o Python
Se ainda não tiver, baixe e instale o Python 3.11 ou superior em [python.org](https://www.python.org/). 
**Importante:** Marque a opção **"Add Python to PATH"** durante a instalação.

## 2. Configurar o Projeto
1. Extraia a pasta do projeto.
2. Abra o **Terminal** (ou PowerShell) dentro da pasta do projeto.
3. Crie um ambiente virtual (opcional, mas recomendado):
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Instale as dependências:
   ```powershell
   pip install -r requirements.txt
   ```

## 3. Rodar o Sistema
No terminal, execute:
```powershell
python app.py
```
O sistema estará disponível em: `http://localhost:5000`

---

# Como subir para o GitHub e colocar na Web

## Passo 1: GitHub
1. Crie um novo repositório no seu GitHub.
2. No terminal da pasta do projeto, execute:
   ```bash
   git init
   git add .
   git commit -m "Primeiro commit - Solução Network"
   git branch -M main
   git remote add origin SEU_LINK_DO_GITHUB_AQUI
   git push -u origin main
   ```

## Passo 2: Colocar na Web (Grátis)
Para que o link funcione na web como o meu, recomendo o **Render.com**:
1. Crie uma conta no [Render.com](https://render.com/).
2. Clique em **"New"** > **"Web Service"**.
3. Conecte seu repositório do GitHub.
4. Nas configurações:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
5. Clique em Deploy e pronto! O Render te dará um link `.onrender.com` público.
