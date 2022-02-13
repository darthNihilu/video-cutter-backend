import os
import threading

from flask import Flask, request, send_from_directory
from flask_cors import CORS

from queStorage import que
from video_cutter import cut_video, remove_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'cutted')
CORS(app)


@app.get('/cutted/<path:path>')
def send_media(path):
    """
    :param path: a path like "posts/<int:post_id>/<filename>"
    """

    return send_from_directory(
        directory=app.config['UPLOAD_FOLDER'], path=path, as_attachment=True
    )


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/cut')
def cutVideo():
    video_url = request.args.get('url')
    start_time = request.args.get('startTime')
    end_time = request.args.get('endTime')

    t1 = threading.Thread(target=cut_video, args=(video_url, float(start_time), float(end_time)))
    t1.start()
    t1.join()

    data = que.get()

    t2 = threading.Thread(target=remove_file, args=[data])
    t2.start()

    return f"/cutted/{data}"
