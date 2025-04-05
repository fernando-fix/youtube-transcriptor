from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/transcription', methods=['GET'])
def get_transcription():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Parâmetro video_id é obrigatório.'}), 400

    try:
        # Obtém a transcrição em português brasileiro
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt-BR'])
        
        # Verifica se o parâmetro "with_times" foi fornecido
        with_times = request.args.get('with_times')
        
        if with_times is None:
            # Se não informar "with_times", retorna a transcrição concatenada sem os tempos
            full_text = " ".join(entry['text'] for entry in transcript)
            return jsonify({'transcription': full_text})
        else:
            # Se informar "with_times", retorna a transcrição com os tempos
            full_text_with_times = " ".join(f"[{entry['start']:.2f}s] {entry['text']}" for entry in transcript)
            return jsonify({'transcription': full_text_with_times})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # A API ficará acessível em todas as interfaces na porta 5000
    app.run(host='0.0.0.0', port=5000)
