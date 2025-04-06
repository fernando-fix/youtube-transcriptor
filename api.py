from flask import Flask, request, jsonify
from flask_cors import CORS
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)
CORS(app)

@app.route('/transcription', methods=['GET'])
def get_transcription():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Parâmetro video_id é obrigatório.'}), 400

    try:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt'])
        except NoTranscriptFound:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['pt-BR'])

        # Verifica se o parâmetro "with_times" foi fornecido
        with_times = request.args.get('with_times')

        if with_times is None:
            full_text = " ".join(entry['text'] for entry in transcript)
            return jsonify({'transcription': full_text})
        else:
            full_text_with_times = " ".join(f"[{entry['start']:.2f}s] {entry['text']}" for entry in transcript)
            return jsonify({'transcription': full_text_with_times})

    except TranscriptsDisabled:
        return jsonify({'error': 'As transcrições estão desativadas para este vídeo.'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'Nenhuma transcrição disponível para esse vídeo.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
