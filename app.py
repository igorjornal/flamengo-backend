from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

def buscar_globoesporte():
    url = 'https://globoesporte.globo.com/futebol/times/flamengo/'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for noticia in soup.find_all('a', class_='feed-post-link'):
        noticias.append({
            'titulo': noticia.text.strip(),
            'url': noticia.get('href'),
            'resumo': '',
            'fonte': 'Globo Esporte'
        })
    return noticias[:10]

def buscar_colunadofla():
    url = 'https://colunadofla.com/ultimas-noticias/'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for noticia in soup.select('.lista-ultimas-noticias article a'):
        noticias.append({
            'titulo': noticia.text.strip(),
            'url': 'https://colunadofla.com' + noticia.get('href'),
            'resumo': '',
            'fonte': 'Coluna do Fla'
        })
    return noticias[:10]

def buscar_lancenet():
    url = 'https://www.lance.com.br/flamengo'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for noticia in soup.select('.feed-list-figure a'):
        noticias.append({
            'titulo': noticia.get('title', '').strip(),
            'url': noticia.get('href', ''),
            'resumo': '',
            'fonte': 'Lancenet'
        })
    return noticias[:10]

def buscar_cnnbrasil():
    url = 'https://www.cnnbrasil.com.br/esportes/futebol/flamengo/'
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    noticias = []
    for noticia in soup.select('.home__list__item'):
        titulo = noticia.select_one('h2')
        link = noticia.select_one('a')
        if titulo and link:
            noticias.append({
                'titulo': titulo.text.strip(),
                'url': link.get('href'),
                'resumo': '',
                'fonte': 'CNN Brasil'
            })
    return noticias[:10]

@app.route('/')
def home():
    return "Backend do Flamengo News está funcionando!"

@app.route('/pesquisar', methods=['POST'])
def pesquisar_noticias():
    noticias = []
    noticias += buscar_globoesporte()
    noticias += buscar_colunadofla()
    noticias += buscar_lancenet()
    noticias += buscar_cnnbrasil()
    return jsonify({'noticias': noticias})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
