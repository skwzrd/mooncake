import os
from datetime import timedelta

directory = os.path.dirname(os.path.abspath(__file__))


def make_path(*filename):
    path = os.path.join(directory, *filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return os.path.abspath(path)


img_path = make_path('static', 'img_uploads')
log_path = make_path('logs', 'app.log')

static_path = os.path.join(directory, 'static')
static_url_path = '/'
template_path = os.path.join(directory, 'static')

session_path = make_path('sessions')
session_type = 'filesystem'
session_lifetime = timedelta(days=2)

translations_path = os.path.join(
    directory, '..', 'translations', 'chinese_hsk_level_1_to_6.csv'
)

audio_path = os.path.join(directory, '..', 'audio', 'vocabulary')

init_sql_path = os.path.join(directory, 'db', 'init.sql')
db_path = os.path.join(directory, 'db', 'mooncake.db')


# defaults for study session
default_hsk = 1
default_size = 10
default_study_session_type = 'equally_mixed'
default_user_id = 1
