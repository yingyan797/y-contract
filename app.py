import os
from webbrowser import get
from flask import Flask, render_template, request, jsonify, g
from werkzeug.utils import secure_filename
import time # For simulating AI response delay
from data_util import Database

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Directory to save uploaded files
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload size

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db():
    if 'db' not in g:
        g.db = Database("session.db")
    g.db.start()
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        print("Database closed")
        db._con.close()
# --- Langchain Placeholder ---
def get_ai_response_langchain_placeholder(user_message, attached_files_info=None):
    """
    Placeholder function for Langchain integration.
    This function would interact with a Langchain agent/chain.
    """
    print(f"User message for AI: {user_message}")
    print(f"Attached files for context: {attached_files_info}")

    # Simulate AI processing time
    time.sleep(1.5)

    # Basic, non-Langchain response for demonstration
    if "hello" in user_message.lower():
        return "Hello! How can I assist you with your legal contracts today?"
    elif "contract" in user_message.lower() and attached_files_info:
        return f"I see you mentioned 'contract' and have attached files like {', '.join(attached_files_info)}. Please specify what you'd like to analyze or discuss about them."
    elif "contract" in user_message.lower():
        return "Please tell me more about the contract you're referring to, or attach the document for analysis."
    elif "thank you" in user_message.lower() or "thanks" in user_message.lower():
        return "You're welcome! Feel free to ask if you have more questions."
    else:
        return "I'm designed to help with legal contract queries. Could you please rephrase your question or provide more details?"

# --- Flask Routes ---
@app.route('/contract')
def index():
    """Renders the main chat interface."""
    return render_template('contract.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """Handles incoming chat messages and generates AI response."""
    data = request.json
    user_message = data.get('message', '')
    attached_files = data.get('attached_files', []) # List of filenames sent from frontend
    session_id = data.get('session_id')
    rank = data.get('rank')

    db = get_db()
    
    # Create new session if none provided
    if not session_id:
        session_id = db.create_session()

    # Save user message to database
    db.save_message(session_id, 'user', rank, user_message)

    # Call the Langchain placeholder
    ai_response = get_ai_response_langchain_placeholder(user_message, attached_files)
    # Save AI response to database
    db.save_message(session_id, 'assistant', rank+1, ai_response)

    return jsonify({'ai_response': ai_response, 'session_id': session_id})

@app.route('/upload_file', methods=['POST'])
def upload_file():
    """Handles file uploads."""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(f"File '{filename}' saved to {filepath}")
        # In a real application, you'd likely process this file
        # (e.g., store metadata in a DB, pass to Langchain for processing)
        return jsonify({'message': f'File {filename} uploaded successfully.', 'filename': filename}), 200
    
    return jsonify({'error': 'File upload failed'}), 500

# Optional: Route to serve file content for overview (if needed from backend)
@app.route('/get_file_content/<filename>')
def get_file_content(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
        except Exception as e:
            return jsonify({'error': f'Could not read file content: {str(e)}'}), 500
    return jsonify({'error': 'File not found'}), 404

@app.route('/get_sessions')
def get_sessions():
    db = get_db()
    results = db('SELECT id, title FROM session ORDER BY created_at DESC')
    sessions = [{'id': row[0], 'title': row[1]} for row in results]
    return jsonify(sessions)

@app.route('/get_session/<int:session_id>')
def get_session(session_id):
    db = get_db()
    results = db('SELECT role, content, rank FROM message WHERE session_id = ? ORDER BY rank', 
                   (session_id,))
    title = db("Select title from session where id=?", (session_id,))
    messages = [{'role': row[0], 'content': row[1], 'rank': row[2]} for row in results]
    return jsonify({"title": title, "messages": messages})

@app.route('/new_session', methods=['POST'])
def new_session():
    db = get_db()
    session_id = db.create_session()
    return jsonify({'session_id': session_id})

@app.route('/rename_session/<int:session_id>', methods=['POST'])
def rename_session(session_id):
    data = request.json
    title = data.get("title")
    db = get_db()
    db("Update session Set title=? Where id=?", (title, session_id,), fetch_num=None)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(port=5002, debug=True)