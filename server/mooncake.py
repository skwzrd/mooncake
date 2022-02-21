from flask import Flask, render_template, jsonify, send_from_directory, abort, request
from api import get_study_session, update_character_stat
import os
from flask_session import Session
from config import (
    audio_path,
    static_url_path,
    template_path,
    session_path,
    session_type,
    session_lifetime,
    default_hsk,
    default_size,
    default_study_session_type,
)
from flask_cors import CORS
import json

app = Flask(__name__, template_folder=template_path, static_url_path=static_url_path)
app.secret_key = str(os.urandom(32))

cors = CORS(app)

app.config['SESSION_TYPE'] = session_type
app.config['PERMANENT_SESSION_LIFETIME'] = session_lifetime
app.config['SESSION_FILE_DIR'] = session_path
app.config['audio_path'] = audio_path
sess = Session()
sess.init_app(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/study_session', methods=['GET', 'POST'])
def study_session():
    """Gets characters to study for a study session.
    GET and POST request parameters:
    - `type`
        - description: the type of study session desired
        - default: `equally_mixed`
        - required: False
        - supported values:
            - `new` new words only
            - `known` known words only
            - `equally_mixed` half new words and half known words (if possible)
    - `size`
        - description: the number of characters to return
        - default: `10`
        - required: False
        - supported values:
            - 1 to 4993
    - `hsk`
        - description: the hsk level to filter by
        - default: `1`
        - required: False
        - supported values:
            - 1 to 6
    """
    if request.method == 'GET':
        hsk = request.args.get('hsk', default_hsk, type=int)
        study_session_type = request.args.get('type', default_study_session_type)
        size = request.args.get('size', default_size, type=int)

    if request.method == 'POST':
        hsk = request.form.get('hsk', default_hsk, type=int)
        study_session_type = request.form.get(
            'study_session_type', default_study_session_type
        )
        size = request.form.get('size', default_size, type=int)

    if hsk < 1 or hsk > 6:
        hsk = 1

    if study_session_type not in {'equally_mixed', 'known', 'new'}:
        study_session_type = default_study_session_type

    if size < 1 or size > 5000:
        size = default_size

    size = int(request.args.get('size', 10))
    new_study_session = get_study_session(
        hsk=hsk, study_session_type=study_session_type, size=size
    )
    return jsonify(new_study_session)


@app.route('/character_stat', methods=['POST'])
def character_stat():
    """Recieves a stat change (delta) for a specific character and user.
    POST request parameters:
    - `user_id`
        - description: The user id
        - default: `None`
        - required: True
    - `character_id`
        - description: character id to apply the delta to
        - default: `None`
        - required: True
        - supported values:
            - 1 to 4993
    - `delta`
        - description: the change in familiarity with a character
        - default: `None`
        - required: True
        - supported values:
            - 1 to 6
    """
    if request.method == 'POST':
        request.data = json.loads(request.data.decode())
        user_id = int(request.data.get('user_id', None))
        character_id = int(request.data.get('character_id', None))
        delta = int(request.data.get('delta', None))

    if None in [user_id, character_id, delta]:
        return abort(400)

    response = update_character_stat(user_id, character_id, delta)
    return jsonify(response)


@app.route('/audio/<string:character>', methods=['GET'])
def character_audio(character: str = None):
    """Recieves a character through the route and returns the mp3 file for it, if it exists.
    """
    if character is None:
        return abort(404)
    return send_from_directory(
        app.config['audio_path'], path=character + '.mp3', mimetype='audio/mp3'
    )


app.run(host='0.0.0.0')
