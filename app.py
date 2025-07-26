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

def download_video(url, output_path):
    ydl_opts = {
        'format': 'best[height<=1080]/best',  # Meilleure qualité jusqu'à 1080p
        'outtmpl': output_path,
        'quiet': True,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return True

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
        download_video(url, video_filename)
        
        tasks[task_id]['status'] = 'analyzing'
        tasks[task_id]['progress'] = 30
        
        # Analyser la vidéo
        best_moments = analyze_audio_peaks(video_filename)
        
        if not best_moments:
            best_moments = [{'start_time': 0, 'rms_level': -30}]
        
        tasks[task_id]['status'] = 'generating'
        tasks[task_id]['progress'] = 50
        tasks[task_id]['clips'] = []
        
        # Générer les clips
        max_clips = min(len(best_moments), num_clips)
        for i in range(max_clips):
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
        
        tasks[task_id]['status'] = 'completed'
        tasks[task_id]['progress'] = 100
        
    except Exception as e:
        tasks[task_id]['status'] = 'error'
        tasks[task_id]['error'] = str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_clips():
    data = request.json
    url = data.get('url')
    duration = float(data.get('duration', 30))
    num_clips = int(data.get('num_clips', 3))
    
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

@app.route('/status/<task_id>')
def get_status(task_id):
    if task_id in tasks:
        return jsonify(tasks[task_id])
    return jsonify({'status': 'not_found'}), 404

@app.route('/download/<filename>')
def download_clip(filename):
    return send_file(f'clips/{filename}', as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'True').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)
