# 🎵 AudioFlow

> A lightweight web-based music player built with Flask that lets users search for songs, play audio previews, upload local MP3 files, and organize tracks into personal playlists.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

### 🎧 Music Search & Playback
- Search for songs directly from the web interface.
- Uses the **iTunes Search API** to retrieve song metadata and available audio previews.
- Displays:
  - Song title
  - Artist
  - Album artwork
  - Audio preview
- Browser-based audio player with:
  - Play / pause
  - Previous / next track
  - Progress tracking
  - Seek control
  - Current and total duration
  - Automatic next-track playback

### 📁 Local MP3 Library
- Upload `.mp3` files through the web interface.
- Uploaded tracks are stored in `static/uploads/`.
- Automatically detects available local MP3 files.
- Local tracks can be played directly in the browser.

### 👤 User Authentication
- User registration and login.
- Passwords are stored as secure password hashes using Werkzeug.
- Session-based authentication with Flask-Login.
- Logout functionality.
- Authentication-protected playlist operations.

### 📚 Personal Playlists
- Create custom playlists after logging in.
- Save searched songs to a playlist.
- View songs stored in individual playlists.
- Each playlist belongs to its authenticated user.
- Server-side authorization prevents users from accessing another user's playlists.

### 🎨 Modern Music-Player UI
- Dark music-player inspired interface.
- Responsive card-based search results.
- Sidebar library and playlist navigation.
- Album artwork cards.
- Persistent bottom audio player.
- Font Awesome icons for controls.

---

## 🖥️ Application Preview

AudioFlow provides a single-page music experience with four main areas:

```text
┌─────────────────────────────────────────────────────────────┐
│ AudioFlow        Search                         Login/Sign Up│
├───────────────┬─────────────────────────────────────────────┤
│ Library       │                                             │
│               │              Search Results                  │
│ Playlists     │        ┌──────┐ ┌──────┐ ┌──────┐           │
│               │        │ Song │ │ Song │ │ Song │           │
│ + New Playlist│        │ Card │ │ Card │ │ Card │           │
│               │        └──────┘ └──────┘ └──────┘           │
├───────────────┴─────────────────────────────────────────────┤
│  Cover   Now Playing          ◀  ▶  ▶        ──── Progress  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| Database | SQLite |
| ORM | Flask-SQLAlchemy |
| Authentication | Flask-Login |
| Password Security | Werkzeug |
| External Music Search | iTunes Search API |
| Frontend | HTML, CSS, JavaScript |
| Icons | Font Awesome |
| Audio | HTML5 Audio API |
| HTTP Requests | Requests |

---

## 📂 Project Structure

```text
Audioflow-App/
│
├── app.py                  # Flask application and API routes
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
│
├── templates/
│   └── index.html          # Main frontend interface
│
├── static/
│   └── uploads/            # Local MP3 uploads
│
└── instance/
    └── music.db            # SQLite database created by Flask
```

> `instance/`, database files, and uploaded MP3 files are intentionally excluded from Git through `.gitignore`.

---

## ⚙️ How It Works

### 1. Music Search

When a user searches for a track:

```text
User enters query
       ↓
Frontend sends /api/search?q=...
       ↓
Flask requests iTunes Search API
       ↓
Song metadata + preview URLs returned
       ↓
Frontend renders song cards
       ↓
User selects a track
       ↓
HTML5 Audio API plays the preview
```

The application requests up to 12 song results and keeps results that provide an audio preview URL.

### 2. Local Music

```text
MP3 Upload
    ↓
Flask /upload endpoint
    ↓
File saved in static/uploads/
    ↓
/api/local_songs scans the folder
    ↓
Track appears in Library
    ↓
Browser plays local file
```

### 3. Authentication

```text
Register
   ↓
Password hashed with Werkzeug
   ↓
User stored in SQLite
   ↓
Login
   ↓
Flask-Login session
   ↓
Access personal playlists
```

### 4. Playlist Flow

```text
Search Song
     ↓
Create Playlist
     ↓
Save Song
     ↓
Song stored in SQLite
     ↓
Load Playlist
     ↓
Play saved tracks
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have installed:

- Python 3.10 or newer
- pip
- Git

Check your Python installation:

```bash
python --version
```

---

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Audioflow-App
```

### 2. Create a Virtual Environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python app.py
```

The Flask development server will start on:

```text
http://127.0.0.1:5000
```

Open that address in your browser.

The SQLite database is automatically initialized when the application starts.

---

## 🔐 Authentication & Playlists

To use personal playlists:

1. Open AudioFlow.
2. Enter a username and password.
3. Click **Sign Up**.
4. Log in using the newly created account.
5. Click **+ New Playlist**.
6. Give the playlist a name.
7. Search for music.
8. Use the `+` button on a song to save it.
9. Select the playlist ID shown in the prompt.
10. Open the playlist from the sidebar to view saved songs.

---

## 🎵 Local MP3 Upload

After logging in:

1. Click the **MP3** upload button.
2. Select an `.mp3` file.
3. AudioFlow uploads it to the local `static/uploads/` directory.
4. Refreshing the library is handled automatically.
5. Select the uploaded track to play it.

### Supported Format

```text
.mp3
```

The current implementation does not include a full audio transcoding pipeline, so uploaded files are expected to already be playable MP3 files.

---

## 🔌 API Endpoints

AudioFlow exposes a small Flask API used by the frontend.

### General

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/` | Serve the main application |
| `POST` | `/upload` | Upload an MP3 file |
| `GET` | `/api/local_songs` | Get locally uploaded songs |
| `GET` | `/api/search?q=<query>` | Search iTunes music |

### Authentication

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/api/auth/register` | Register a user |
| `POST` | `/api/auth/login` | Log in |
| `GET` | `/api/auth/logout` | Log out |
| `GET` | `/api/auth/status` | Check authentication status |

### Playlists

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/playlists` | Get current user's playlists |
| `POST` | `/api/playlists` | Create a playlist |
| `POST` | `/api/playlists/<id>/add` | Add a song to a playlist |
| `GET` | `/api/playlists/<id>/songs` | Get songs from a playlist |

---

## 🗄️ Database Schema

AudioFlow uses three main SQLite models:

### User

```text
User
├── id
├── username
└── password_hash
```

### Playlist

```text
Playlist
├── id
├── name
└── user_id → User
```

### Song

```text
Song
├── id
├── title
├── artist
├── url
├── cover
└── playlist_id → Playlist
```

Relationship:

```text
User
 │
 └───< Playlist
          │
          └───< Song
```

---

## 🔒 Security Notes

The project includes several useful security practices, including:

- Password hashing with Werkzeug.
- Login-required protection for playlist routes.
- User ownership checks before playlist access.
- SQLite database and uploaded media excluded from Git through `.gitignore`.

### Before Production Deployment

The current project is primarily a learning/development application. For production use, consider:

- Move the Flask secret key into an environment variable.
- Run Flask with `debug=False`.
- Validate and sanitize uploaded filenames with `secure_filename`.
- Restrict upload size and MIME/type validation.
- Protect the upload endpoint with authentication.
- Add CSRF protection for state-changing browser requests.
- Add stronger input validation for usernames, passwords, playlist names, and API payloads.
- Consider a production database such as PostgreSQL for larger deployments.
- Add rate limiting to authentication and API endpoints.
- Avoid exposing uploaded files without appropriate access controls if private media is intended.

---

## 📦 Dependencies

The application currently uses:

```text
Flask==3.0.0
requests==2.31.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
Werkzeug==3.0.1
```

Install them with:

```bash
pip install -r requirements.txt
```

---

## 🧪 Current Scope

AudioFlow currently focuses on:

- Music discovery through searchable song metadata and previews
- Local MP3 playback
- Basic user accounts
- Personal playlists
- Browser-based audio controls

It does **not** currently implement features such as:

- Full-length commercial music streaming
- Music downloads
- Advanced recommendation algorithms
- Social following/sharing
- Cloud storage
- Mobile applications
- Automatic audio transcoding

---

## 🔮 Future Improvements

Potential extensions include:

- 🎚️ Volume and mute controls
- 🔀 Shuffle and repeat modes
- ❤️ Favorites / liked songs
- 🔍 Advanced search filters
- 🎵 Album and artist pages
- 📱 Improved mobile responsiveness
- 🎨 Custom playlist covers
- 🗑️ Delete and rename playlists
- ➕ Better song-to-playlist selection UI instead of playlist ID prompts
- 📊 Listening history and statistics
- 🤖 Personalized music recommendations
- ☁️ Cloud-based music storage
- 🔐 Environment-based production configuration
- 🧪 Automated backend and API tests
- 🚀 Production deployment with Gunicorn and a production database

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Commit them:

```bash
git commit -m "Add your feature"
```

5. Push the branch:

```bash
git push origin feature/your-feature
```

6. Open a Pull Request.

---

## 📜 License

This project is available under the **MIT License**.

You may adapt the license to match the intended distribution of your project.

---

## 👨‍💻 Author

**Ashish Kumar Mishra**

- GitHub: [ash972-cpu](https://github.com/ash972-cpu)
- LinkedIn: [Ashish Kumar Mishra](https://www.linkedin.com/in/ashish-kumar-mishra-9837a129/)

---

## ⭐ If You Like the Project

If AudioFlow helped you learn or inspired you to build something similar, consider giving the repository a ⭐ on GitHub.
