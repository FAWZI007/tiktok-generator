from flask import Flask

app = Flask(__name__)

@app.route('/')
def test():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
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
