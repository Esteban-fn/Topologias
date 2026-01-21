# Plataforma de Topologia ISP

Este é um projeto simples e profissional desenvolvido para facilitar a visualização de topologias de rede e resumos técnicos de clientes.

## 🚀 Tecnologias Utilizadas
- **Back-end:** Python + Flask
- **Banco de Dados:** Excel (.xlsx)
- **Front-end:** HTML5, CSS3, Bootstrap 5

## 📂 Estrutura do Projeto
- `app.py`: Arquivo principal com as rotas e lógica do sistema.
- `data/clientes.xlsx`: "Banco de dados" onde ficam as informações dos clientes.
- `static/imagens/`: Pasta para armazenar as imagens das topologias.
- `templates/`: Pasta com os arquivos HTML da interface.

## 🔐 Acesso ao Sistema
- **Usuário:** suporte
- **Senha:** senha123

## 🛠️ Como Adicionar Novos Clientes
1. Abra o arquivo `data/clientes.xlsx`.
2. Adicione uma nova linha com:
   - `id`: Próximo número sequencial.
   - `nome_cliente`: Nome do cliente.
   - `titulo_sistema`: Título que aparecerá no topo da página.
   - `imagem`: Nome do arquivo de imagem (ex: `cliente3.png`).
   - `resumo`: Texto com as observações técnicas.
3. Coloque a imagem correspondente na pasta `static/imagens/`.
4. O sistema atualizará automaticamente!

## 📦 Instalação
Caso queira rodar em outro ambiente:
```bash
pip install flask pandas openpyxl
python app.py
```
