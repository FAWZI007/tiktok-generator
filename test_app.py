from flask import Flask, jsonify, request
import os
import sys

app = Flask(__name__)

@app.route('/')
def test():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>🧪 Test TikTok Generator</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body>
        <h1>🧪 Test TikTok Generator</h1>
        <p>Test pour diagnostiquer le problème</p>
        
        <button onclick="testHealth()">Test Health</button>
        <button onclick="testGenerate()">Test Generate</button>
        
        <div id="result" style="margin-top: 20px; padding: 10px; border: 1px solid #ccc;"></div>
        
        <script>
        async function testHealth() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '⏳ Test Health...';
            
            try {
                const response = await fetch('/test-health');
                const result = await response.json();
                resultDiv.innerHTML = '<h3>✅ Health OK</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
            } catch (error) {
                resultDiv.innerHTML = '❌ Erreur Health: ' + error.message;
            }
        }
        
        async function testGenerate() {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = '⏳ Test Generate...';
            
            try {
                const response = await fetch('/test-generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        url: 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                        duration: 30,
                        num_clips: 1
                    })
                });
                
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                
                const result = await response.json();
                resultDiv.innerHTML = '<h3>✅ Generate OK</h3><pre>' + JSON.stringify(result, null, 2) + '</pre>';
                
            } catch (error) {
                resultDiv.innerHTML = '❌ Erreur Generate: ' + error.message;
            }
        }
        </script>
    </body>
    </html>
    '''

@app.route('/test-health')
def test_health():
    try:
        return jsonify({
            'status': 'healthy',
            'python_version': sys.version,
            'working_directory': os.getcwd(),
            'files_in_directory': os.listdir('.'),
            'environment_port': os.environ.get('PORT', 'Not set')
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test-generate', methods=['POST'])
def test_generate():
    try:
        data = request.json
        return jsonify({
            'status': 'success',
            'message': 'Generate endpoint fonctionne!',
            'received_data': data,
            'validation': 'URL validation would happen here'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        <title>Test TikTok Generator</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>
    <body style="font-family: Arial; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh;">
        <div style="max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 20px;">
            <h1 style="text-align: center; color: #333;">🎬 Test TikTok Generator</h1>
            <p style="text-align: center; color: #666;">Application de test fonctionnelle !</p>
            <div style="background: #f0f8ff; padding: 15px; border-radius: 10px; margin-top: 20px;">
                <p><strong>✅ Flask fonctionne !</strong></p>
                <p><strong>✅ Interface mobile OK !</strong></p>
                <p><strong>✅ Prêt pour les fonctionnalités complètes !</strong></p>
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    print("🚀 Lancement du serveur de test...")
    app.run(host='0.0.0.0', port=5000, debug=True)
