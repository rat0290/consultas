from flask import Flask, render_template, request
import os
import requests

# A inicialização do Flask para rodar no ambiente serverless da Vercel
app = Flask(__name__, template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'templates'))

# Função para encontrar o CPF baseado no telefone
def encontrar_cpf_por_telefone(telefone):
    try:
        with open('dados.txt', 'r') as file:
            for line in file:
                cpf, telefone_atual = line.strip().split(',')
                if telefone == telefone_atual:
                    return cpf
    except FileNotFoundError:
        return None

# Função para consultar a API com o CPF
def consultar_api_cpf(cpf):
    # Sua API com a URL fornecida
    url = f'https://sitedoaplicativo.xyz:8443/?port=3000&id=consulta&key=COD-IJKHSADU&tp=cpf&cpf={cpf}'
    
    try:
        # Envia a requisição para a API e obtém a resposta
        response = requests.get(url)
        # Checa se a resposta foi bem-sucedida (status code 200)
        if response.status_code == 200:
            dados = response.json()
            # Acessa o objeto 'DadosBasicos' que contém as informações desejadas
            if 'DadosBasicos' in dados:
                return dados['DadosBasicos']  # Retorna os dados básicos do CPF
            else:
                return None
        else:
            return None
    except Exception as e:
        print(f"Erro ao consultar API: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        telefone = request.form['telefone']
        cpf = encontrar_cpf_por_telefone(telefone)
        if cpf:
            # Consultar a API usando o CPF encontrado
            dados_api = consultar_api_cpf(cpf)
            if dados_api:
                return render_template('index.html', cpf=cpf, telefone=telefone, dados=dados_api)
            else:
                return render_template('index.html', cpf=cpf, telefone=telefone, erro="Não foi possível consultar os dados na API.")
        else:
            return render_template('index.html', erro="Telefone não encontrado.")
    return render_template('index.html')

# Para a Vercel, usamos uma função que exporta o app
def handler(request):
    with app.app_context():
        return app.full_dispatch_request()

if __name__ == '__main__':
    app.run(debug=True)
