import subprocess
import re 
from yt_dlp import YoutubeDL

def download_video(url, output_path='video.mp4'):
    ydl_opts = {
        'format': 'best[height<=1080]/best',  # Meilleure qualité jusqu'à 1080p
        'outtmpl': output_path,
        'quiet': True,
        # Options pour préserver la qualité
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"Vidéo haute qualité téléchargée: {output_path}")

def analyze_audio_peaks(video_file, segment_duration=10, min_gap=5):
    """
    Analyse la vidéo par segments pour trouver les moments les plus forts
    segment_duration: durée de chaque segment analysé (en secondes)
    min_gap: écart minimum entre deux moments détectés (en secondes)
    """
    # D'abord, obtenir la durée totale de la vidéo
    cmd = [
        'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', video_file
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        total_duration = float(result.stdout.strip())
    except:
        print("Impossible de déterminer la durée de la vidéo, utilisation de 300s par défaut")
        total_duration = 300
    
    print(f"Durée totale de la vidéo: {total_duration:.1f} secondes")
    
    # Analyser chaque segment
    segments = []
    current_time = 0
    
    while current_time < total_duration:
        # Analyser le volume RMS de ce segment
        cmd = [
            'ffmpeg', '-ss', str(current_time), '-i', video_file,
            '-t', str(segment_duration), '-af', 'volumedetect',
            '-f', 'null', '-'
        ]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        
        # Extraire le niveau RMS moyen
        rms_level = -60  # valeur par défaut (très faible)
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
        print(f"Analysé: {current_time:.1f}s/{total_duration:.1f}s", end='\r')
    
    print()  # nouvelle ligne
    
    # Trier par niveau de volume (du plus fort au plus faible)
    segments.sort(key=lambda x: x['rms_level'], reverse=True)
    
    # Sélectionner les meilleurs moments en évitant les chevauchements
    best_moments = []
    for segment in segments:
        # Vérifier qu'il n'y a pas de chevauchement avec les moments déjà sélectionnés
        overlap = False
        for existing in best_moments:
            if (abs(segment['start_time'] - existing['start_time']) < min_gap):
                overlap = True
                break
        
        if not overlap and segment['rms_level'] > -40:  # Seuil de volume minimum
            best_moments.append(segment)
            
        # Limiter à 5 meilleurs moments
        if len(best_moments) >= 5:
            break
    
    # Trier les moments sélectionnés par ordre chronologique
    best_moments.sort(key=lambda x: x['start_time'])
    
    return best_moments

def find_best_moments(video_file):
    """Trouve automatiquement les meilleurs moments de la vidéo"""
    print("🔍 Analyse de la vidéo en cours...")
    best_moments = analyze_audio_peaks(video_file)
    
    if not best_moments:
        print("⚠️ Aucun moment fort détecté, utilisation du début de la vidéo")
        return [{'start_time': 0, 'rms_level': -30}]
    
    print(f"✓ {len(best_moments)} moment(s) fort(s) détecté(s):")
    for i, moment in enumerate(best_moments, 1):
        minutes = int(moment['start_time'] // 60)
        seconds = int(moment['start_time'] % 60)
        print(f"  {i}. {minutes:02d}:{seconds:02d} (niveau: {moment['rms_level']:.1f}dB)")
    
    return best_moments

def cut_clip(input_file, start_time, duration, output_file='clip.mp4'):
    cmd = [
        'ffmpeg',
        '-ss', str(start_time),
        '-i', input_file,
        '-t', str(duration),
        # Amélioration de la qualité vidéo
        '-vf', 'scale=720:1280:flags=lanczos,setsar=1',  # Meilleur algorithme de redimensionnement
        '-c:v', 'libx264',           # Codec vidéo de haute qualité
        '-preset', 'slow',           # Preset pour meilleure qualité (plus lent mais meilleur)
        '-crf', '18',               # Facteur de qualité constant (18 = très haute qualité)
        '-profile:v', 'high',        # Profil H.264 haute qualité
        '-level:v', '4.1',          # Niveau de compatibilité
        '-pix_fmt', 'yuv420p',      # Format de pixel compatible
        # Amélioration de l'audio
        '-c:a', 'aac',              # Codec audio de qualité
        '-b:a', '128k',             # Bitrate audio élevé
        '-ar', '44100',             # Fréquence d'échantillonnage standard
        '-ac', '2',                 # Stéréo
        # Options générales
        '-movflags', '+faststart',   # Optimisation pour streaming
        '-y',                       # Remplacer le fichier de sortie
        output_file
    ]
    subprocess.run(cmd, check=True)
    print(f"Clip haute qualité sauvegardé: {output_file}")

if __name__ == "__main__":
    # Télécharger la vidéo une seule fois
    url = input("Lien YouTube: ")
    video_filename = 'video.mp4'
    download_video(url, video_filename)
    
    # Analyser automatiquement la vidéo pour trouver les meilleurs moments
    best_moments = find_best_moments(video_filename)
    
    # Demander la durée des clips
    duration = float(input("\nDurée de chaque clip en secondes: "))
    
    # Demander combien de clips générer
    max_clips = min(len(best_moments), int(input(f"Combien de clips générer? (max {len(best_moments)}): ")))
    
    print(f"\n🎬 Génération de {max_clips} clip(s)...")
    
    # Générer automatiquement les clips pour les meilleurs moments
    for i in range(max_clips):
        moment = best_moments[i]
        start_time = moment['start_time']
        clip_filename = f'clip_{i+1}.mp4'
        
        try:
            minutes = int(start_time // 60)
            seconds = int(start_time % 60)
            print(f"\n📹 Clip {i+1}: début à {minutes:02d}:{seconds:02d}")
            cut_clip(video_filename, start_time, duration, clip_filename)
            print(f"✓ Clip {i+1} généré avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur lors de la génération du clip {i+1}: {e}")
    
    print(f"\n🎉 Terminé! {max_clips} clip(s) généré(s) automatiquement à partir des meilleurs moments.")
