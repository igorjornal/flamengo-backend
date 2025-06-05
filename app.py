from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
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
    url = 'https://globoesporte.globo.com/futebol/times/flamengo/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for noticia in soup.find_all('a', class_='feed-post-link'):
        noticias.append({
            'titulo': noticia.text.strip(),
            'url': noticia.get('href'),
            'resumo': '',  # O Globo Esporte não mostra resumo na lista
            'fonte': 'Globo Esporte'
        })
    return jsonify({'noticias': noticias[:10]})  # Limita a 10 notícias

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
