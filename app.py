from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import pandas as pd
import requests
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_super_segura'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['PROCESSED_FOLDER'] = 'processed'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Garantir que as pastas existam
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

# ========= ROTAS =========
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # Verificar se o arquivo foi enviado
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado!')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Validar nome do arquivo
    if file.filename == '':
        flash('Nome de arquivo inválido!')
        return redirect(url_for('index'))
    
    # Validar extensão
    if not allowed_file(file.filename):
        flash('Apenas arquivos .xlsx são permitidos!')
        return redirect(url_for('index'))
    
    # Salvar arquivo
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Processar arquivo
    try:
        processed_filename = processar_arquivo(filepath)
        return redirect(url_for('processando', filename=processed_filename))
    except Exception as e:
        flash(f'Erro no processamento: {str(e)}')
        return redirect(url_for('index'))

@app.route('/processando/<filename>')
def processando(filename):
    return render_template('processando.html', filename=filename)

@app.route('/download/<filename>')
def download(filename):
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(processed_path, as_attachment=True)

# ========= FUNÇÕES AUXILIARES =========
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'xlsx'}

def consultar_cnpj(cnpj, session):
    url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj}"
    try:
        response = session.get(url, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro na consulta do CNPJ {cnpj}: {str(e)}")
        return None

def processar_arquivo(filepath):
    # Ler arquivo
    df = pd.read_excel(filepath, dtype=str)
    
    # Validar colunas
    required_columns = ["RAZÃO SOCIAL", "CNPJ", "SITUAÇÃO CADASTRAL", "CNAE", "PORTE"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("A planilha deve conter todas as colunas obrigatórias!")
    
    # Processar CNPJs
    with requests.Session() as session:
        for index, row in df.iterrows():
            if pd.isna(row['SITUAÇÃO CADASTRAL']) or row['SITUAÇÃO CADASTRAL'] == '':
                cnpj = str(row['CNPJ']).zfill(14)
                
                print(f"Processando CNPJ: {cnpj}")
                dados = consultar_cnpj(cnpj, session)
                
                if dados:
                    df.at[index, 'SITUAÇÃO CADASTRAL'] = dados.get('descricao_situacao_cadastral', 'Erro')
                    df.at[index, 'CNAE'] = dados.get('cnae_fiscal_descricao', 'Erro')
                    df.at[index, 'PORTE'] = dados.get('porte', 'Erro')
                
                time.sleep(1)  # Evitar bloqueio por excesso de requisições
    
    # Salvar arquivo processado
    processed_filename = f"processed_{secure_filename(os.path.basename(filepath))}"
    processed_path = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
    df.to_excel(processed_path, index=False)
    
    return processed_filename

if __name__ == '__main__':
    app.run(debug=True)