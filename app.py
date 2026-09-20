from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import requests

app = Flask(__name__)

# --- Configuration ---
app.secret_key = 'super_secret_production_key_here' # Change this in production
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# --- Initialize Extensions ---
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Models ---
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    playlists = db.relationship('Playlist', backref='owner', lazy=True)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    songs = db.relationship('Song', backref='playlist', lazy=True)

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    artist = db.Column(db.String(100))
    url = db.Column(db.String(500), nullable=False)
    cover = db.Column(db.String(500))
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'), nullable=False)

with app.app_context():
    db.create_all()

# --- Core Routes ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file and file.filename.endswith('.mp3'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        return jsonify({'message': 'Uploaded', 'url': f'/static/uploads/{file.filename}'})
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/api/local_songs')
def local_songs():
    songs = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if filename.endswith('.mp3'):
            songs.append({
                'title': filename, 'artist': 'Local File',
                'url': f'/static/uploads/{filename}',
                'cover': 'https://placehold.co/150x150/1db954/white?text=Local'
            })
    return jsonify(songs)

@app.route('/api/search')
def search():
    query = request.args.get('q')
    if not query: return jsonify([])
    try:
        url = f"https://itunes.apple.com/search?term={query}&entity=song&limit=12"
        response = requests.get(url).json()
        
        results = []
        for item in response.get('results', []):
            if item.get('previewUrl'): # Ensure the track has an audio preview
                results.append({
                    'title': item.get('trackName', 'Unknown'),
                    'artist': item.get('artistName', 'Unknown'),
                    'url': item.get('previewUrl'),
                    'cover': item.get('artworkUrl100', 'https://placehold.co/150x150/1db954/white?text=Music')
                })
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- Auth Routes ---
@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username exists'}), 400
    db.session.add(User(username=data['username'], password_hash=generate_password_hash(data['password'])))
    db.session.commit()
    return jsonify({'message': 'Registered'})

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in', 'username': user.username})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/auth/status')
def auth_status():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'username': current_user.username})
    return jsonify({'logged_in': False})

# --- Playlist Routes ---
@app.route('/api/playlists', methods=['GET', 'POST'])
@login_required
def manage_playlists():
    if request.method == 'POST':
        db.session.add(Playlist(name=request.json['name'], user_id=current_user.id))
        db.session.commit()
        return jsonify({'message': 'Created'})
    return jsonify([{'id': p.id, 'name': p.name} for p in Playlist.query.filter_by(user_id=current_user.id).all()])

@app.route('/api/playlists/<int:playlist_id>/add', methods=['POST'])
@login_required
def add_to_playlist(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    data = request.json
    db.session.add(Song(title=data['title'], artist=data.get('artist', ''), url=data['url'], cover=data.get('cover', ''), playlist_id=playlist_id))
    db.session.commit()
    return jsonify({'message': 'Added'})

@app.route('/api/playlists/<int:playlist_id>/songs')
@login_required
def get_playlist_songs(playlist_id):
    playlist = Playlist.query.get_or_404(playlist_id)
    if playlist.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify([{'title': s.title, 'artist': s.artist, 'url': s.url, 'cover': s.cover} for s in playlist.songs])

if __name__ == '__main__':
    app.run(debug=True, port=5000)