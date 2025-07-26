from flask import Flask, render_template, request, jsonify, send_file, url_for
import subprocess
import os
import threading
import time
from yt_dlp import YoutubeDL
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'clips'

# Créer le dossier clips s'il n'existe pas
os.makedirs('clips', exist_ok=True)
os.makedirs('videos', exist_ok=True)

# Route de santé pour Railway
@app.route('/health')
def health():
    return {'status': 'healthy', 'message': 'TikTok Generator is running!'}

# Stockage des tâches en cours
tasks = {}

# Fonction pour nettoyer les anciens fichiers au démarrage
def cleanup_old_files():
    try:
        # Nettoyer les anciens clips
        for filename in os.listdir('clips'):
            if filename.endswith('.mp4'):
                os.remove(os.path.join('clips', filename))
        
        # Nettoyer les anciennes vidéos
        for filename in os.listdir('videos'):
            if filename.endswith('.mp4'):
                os.remove(os.path.join('videos', filename))
    except Exception as e:
        print(f"Erreur lors du nettoyage: {e}")

# Nettoyer au démarrage
cleanup_old_files()

def download_video(url, output_path):
    try:
        # Valider que l'URL est bien YouTube
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            raise ValueError("URL non supportée. Utilisez une URL YouTube.")
        
        ydl_opts = {
            'format': 'best[height<=1080]/best',  # Meilleure qualité jusqu'à 1080p
            'outtmpl': output_path,
            'quiet': True,
            'writesubtitles': False,
            'writeautomaticsub': False,
            'ignoreerrors': False,  # Ne pas ignorer les erreurs pour mieux diagnostiquer
            'no_warnings': True,
        }
        
        with YoutubeDL(ydl_opts) as ydl:
            # Vérifier d'abord si la vidéo existe
            info = ydl.extract_info(url, download=False)
            if not info:
                raise ValueError("Impossible d'extraire les informations de la vidéo")
            
            # Télécharger la vidéo
            ydl.download([url])
            
            # Vérifier que le fichier a bien été créé
            if not os.path.exists(output_path):
                raise ValueError("Le téléchargement a échoué - fichier non créé")
                
        return True
        
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")
        raise

def analyze_audio_peaks(video_file, segment_duration=10, min_gap=5):
    # Obtenir la durée totale
    cmd = [
        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', video_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        total_duration = float(result.stdout.strip())
    except:
        total_duration = 300
    
    segments = []
    current_time = 0
    
    while current_time < total_duration:
        cmd = [
            'ffmpeg', '-ss', str(current_time), '-i', video_file,
            '-t', str(segment_duration), '-af', 'volumedetect',
            '-f', 'null', '-'
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        
        rms_level = -60
        for line in result.stderr.split('\n'):
            if 'mean_volume:' in line:
                try:
                    rms_level = float(line.split('mean_volume:')[1].split('dB')[0].strip())
                except:
                    pass
        
        segments.append({
            'start_time': current_time,
            'rms_level': rms_level,
            'end_time': min(current_time + segment_duration, total_duration)
        })
        
        current_time += segment_duration
    
    segments.sort(key=lambda x: x['rms_level'], reverse=True)
    
    best_moments = []
    for segment in segments:
        overlap = False
        for existing in best_moments:
            if (abs(segment['start_time'] - existing['start_time']) < min_gap):
                overlap = True
                break
        
        if not overlap and segment['rms_level'] > -40:
            best_moments.append(segment)
            
        if len(best_moments) >= 5:
            break
    
    best_moments.sort(key=lambda x: x['start_time'])
    return best_moments

def cut_clip(input_file, start_time, duration, output_file):
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', input_file,
        '-t', str(duration),
        # Configuration compatible pour serveurs gratuits
        '-vf', 'scale=720:1280',    # Redimensionnement simple
        '-c:v', 'libx264',          # Codec vidéo standard
        '-preset', 'fast',          # Preset rapide pour serveur gratuit
        '-crf', '23',              # Qualité normale (plus compatible)
        '-pix_fmt', 'yuv420p',     # Format de pixel standard
        # Audio simplifié
        '-c:a', 'aac',             # Codec audio standard
        '-b:a', '96k',             # Bitrate audio normal
        # Options générales
        '-movflags', '+faststart',  # Optimisation pour streaming
        '-y',                       # Remplacer le fichier de sortie
        output_file
    ]
    subprocess.run(cmd, check=True)
    return True

def process_video_task(task_id, url, duration, num_clips):
    try:
        tasks[task_id]['status'] = 'downloading'
        tasks[task_id]['progress'] = 10
        
        # Télécharger la vidéo
        video_filename = f'videos/video_{task_id}.mp4'
        try:
            download_video(url, video_filename)
        except Exception as e:
            raise Exception(f"Impossible de télécharger la vidéo: {str(e)}")
        
        tasks[task_id]['status'] = 'analyzing'
        tasks[task_id]['progress'] = 30
        
        # Analyser la vidéo
        try:
            best_moments = analyze_audio_peaks(video_filename)
        except Exception as e:
            print(f"Erreur analyse audio: {e}")
            best_moments = []
        
        if not best_moments:
            best_moments = [{'start_time': 0, 'rms_level': -30}]
        
        tasks[task_id]['status'] = 'generating'
        tasks[task_id]['progress'] = 50
        tasks[task_id]['clips'] = []
        
        # Générer les clips
        max_clips = min(len(best_moments), num_clips)
        for i in range(max_clips):
            try:
                moment = best_moments[i]
                start_time = moment['start_time']
                clip_filename = f'clips/clip_{task_id}_{i+1}.mp4'
                
                cut_clip(video_filename, start_time, duration, clip_filename)
                
                tasks[task_id]['clips'].append({
                    'filename': f'clip_{task_id}_{i+1}.mp4',
                    'start_time': start_time,
                    'duration': duration
                })
                
                tasks[task_id]['progress'] = 50 + (40 * (i + 1) / max_clips)
                
            except Exception as e:
                print(f"Erreur génération clip {i+1}: {e}")
                continue
        
        if not tasks[task_id]['clips']:
            raise Exception("Aucun clip n'a pu être généré")
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        
    except Exception as e:
        print(f"Erreur dans process_video_task: {e}")
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_clips():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'Aucune donnée JSON reçue'}), 400
            
        url = data.get('url')
        if not url:
            return jsonify({'error': 'URL manquante'}), 400
        
        # Validation stricte de l'URL YouTube
        if not any(domain in url.lower() for domain in ['youtube.com', 'youtu.be']):
            return jsonify({'error': 'URL invalide. Utilisez une URL YouTube (youtube.com ou youtu.be)'}), 400
        
        # Vérifier que l'URL contient bien un ID de vidéo
        if 'youtube.com' in url and 'v=' not in url:
            return jsonify({'error': 'URL YouTube invalide. Assurez-vous qu\'elle contient l\'ID de la vidéo (v=...)'}), 400
        if 'youtu.be' in url and len(url.split('/')[-1]) < 10:
            return jsonify({'error': 'URL YouTube courte invalide'}), 400
            
        duration = float(data.get('duration', 30))
        num_clips = int(data.get('num_clips', 3))
        
        # Valider les paramètres
        if duration < 5 or duration > 120:
            return jsonify({'error': 'Durée invalide (5-120 secondes)'}), 400
        if num_clips < 1 or num_clips > 5:
            return jsonify({'error': 'Nombre de clips invalide (1-5)'}), 400
        
        task_id = str(uuid.uuid4())
        tasks[task_id] = {
            'status': 'pending',
            'progress': 0,
            'clips': []
        }
        
        # Lancer le traitement en arrière-plan
        thread = threading.Thread(target=process_video_task, args=(task_id, url, duration, num_clips))
        thread.start()
        
        return jsonify({'task_id': task_id})
        
    except Exception as e:
        return jsonify({'error': f'Erreur serveur: {str(e)}'}), 500

@app.route('/status/<task_id>')
def get_status(task_id):
    try:
        if task_id in tasks:
            return jsonify(tasks[task_id])
        return jsonify({'status': 'not_found', 'error': 'Task not found'}), 404
    except Exception as e:
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/download/<filename>')
def download_clip(filename):
    return send_file(f'clips/{filename}', as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
