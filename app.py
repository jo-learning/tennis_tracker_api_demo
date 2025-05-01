from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from tracker import track_video

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/api/track', methods=['POST'])
def track():
    if 'video' not in request.files:
        return jsonify({'error': 'No video uploaded'}), 400

    video_file = request.files['video']
    path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(path)

    tracking_data = track_video(path)

    return jsonify(tracking_data)

if __name__ == '__main__':
    app.run(debug=True)
