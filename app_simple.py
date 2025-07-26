from flask import Flask, render_template_string, request, jsonify
import os
import threading
import time
import uuid

app = Flask(__name__)

# Variables globales simplifiées
tasks = {}

# Template HTML simplifié intégré
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>TikTok Generator</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial; padding: 20px; background: #f0f0f0; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        input, button { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #ccc; border-radius: 5px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        .error { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 5px; margin: 10px 0; }
        .success { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 TikTok Generator (Version Simplifiée)</h1>
        
        <form id="testForm">
            <input type="url" id="url" placeholder="URL YouTube" value="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
            <input type="number" id="duration" value="30" min="5" max="60">
            <button type="submit">Test Génération</button>
        </form>
        
        <div id="result"></div>
    </div>
    
    <script>
        document.getElementById('testForm').onsubmit = async function(e) {
            e.preventDefault();
            
            const result = document.getElementById('result');
            result.innerHTML = '<div class="success">⏳ Test en cours...</div>';
            
            try {
                const response = await fetch('/test-simple', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        url: document.getElementById('url').value,
                        duration: document.getElementById('duration').value
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    result.innerHTML = '<div class="success">✅ Test réussi ! L\'application fonctionne.</div>';
                } else {
                    result.innerHTML = '<div class="error">❌ Erreur: ' + data.error + '</div>';
                }
                
            } catch (error) {
                result.innerHTML = '<div class="error">❌ Erreur de connexion: ' + error.message + '</div>';
            }
        };
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'message': 'TikTok Generator is running!'})

@app.route('/test-simple', methods=['POST'])
def test_simple():
    try:
        data = request.json
        url = data.get('url', '')
        duration = data.get('duration', 30)
        
        # Validation simple
        if not url:
            return jsonify({'success': False, 'error': 'URL manquante'})
        
        if 'youtube.com' not in url and 'youtu.be' not in url:
            return jsonify({'success': False, 'error': 'URL YouTube requise'})
        
        # Simulation de traitement (sans yt-dlp pour l'instant)
        return jsonify({
            'success': True, 
            'message': f'URL validée: {url}, durée: {duration}s',
            'note': 'Version simplifiée - pas de téléchargement réel'
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
