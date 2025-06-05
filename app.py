from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend do Flamengo News está funcionando!"

@app.route('/pesquisar', methods=['POST'])
def pesquisar_noticias():
    termo = request.json.get('termo', '')
    if not termo:
        return jsonify({'erro': 'Termo de pesquisa obrigatório'}), 400
    # Simulação de busca (substitua por busca real se quiser)
    return jsonify({
        'termo': termo,
        'noticias': [
            {'titulo': 'Notícia sobre ' + termo, 'resumo': 'Resumo da notícia', 'url': 'https://ge.globo.com/futebol/times/flamengo/'}
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
