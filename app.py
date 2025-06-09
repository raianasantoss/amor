from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Arquivo para armazenar os dados
DATA_FILE = 'data.json'

# Inicializar dados se o arquivo não existir
if not os.path.exists(DATA_FILE):
    initial_data = {
        'dreams': [
            "Viajar para a Europa juntas e conhecer Paris",
            "Morar numa casa com jardim e dois cachorrinhos",
            "Ver o nascer do sol na praia abraçadas",
            "Fazer uma festa de casamento quando pudermos nos assumir",
            "Criar nosso próprio negócio juntas"
        ],
        'watched_movies': [],
        'completed_dates': []
    }
    with open(DATA_FILE, 'w') as f:
        json.dump(initial_data, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_data')
def get_data():
    with open(DATA_FILE, 'r') as f:
        data = json.load(f)
    return jsonify(data)

@app.route('/add_dream', methods=['POST'])
def add_dream():
    new_dream = request.json.get('dream')
    if new_dream:
        with open(DATA_FILE, 'r+') as f:
            data = json.load(f)
            data['dreams'].append(new_dream)
            f.seek(0)
            json.dump(data, f)
            f.truncate()
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/toggle_movie', methods=['POST'])
def toggle_movie():
    movie_id = request.json.get('movie_id')
    action = request.json.get('action')  # 'add' or 'remove'
    
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        
        if action == 'add' and movie_id not in data['watched_movies']:
            data['watched_movies'].append(movie_id)
        elif action == 'remove' and movie_id in data['watched_movies']:
            data['watched_movies'].remove(movie_id)
            
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    
    return jsonify({'success': True})

@app.route('/toggle_date', methods=['POST'])
def toggle_date():
    date_id = request.json.get('date_id')
    action = request.json.get('action')  # 'add' or 'remove'
    
    with open(DATA_FILE, 'r+') as f:
        data = json.load(f)
        
        if action == 'add' and date_id not in data['completed_dates']:
            data['completed_dates'].append(date_id)
        elif action == 'remove' and date_id in data['completed_dates']:
            data['completed_dates'].remove(date_id)
            
        f.seek(0)
        json.dump(data, f)
        f.truncate()
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)