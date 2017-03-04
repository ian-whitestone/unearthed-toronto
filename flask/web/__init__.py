from flask import Flask, request, session, g
from flask_login import current_user
import os
import re
from jinja2 import evalcontextfilter, Markup, escape
from datetime import timedelta

app = Flask(__name__)
app.config["SECRET_KEY"] = "edfAGREjldajfio3453rWEhioew"

ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
UPLOAD_FOLDER = os.path.join(ROOT_PATH, 'flask/web/static/data')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['xls', 'xlsx']
print(UPLOAD_FOLDER)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


########################### SET UP DATABASE ###############################
# DATABASE = os.path.join(app.root_path, '../../sqlite/records.db')

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE, timeout=5)
#         db.row_factory = make_dicts
#     return db
#
# @app.teardown_appcontext
# def close_connection(exception):
#     db = getattr(g, '_database', None)
#     if db is not None:
#         db.close()
#
# with app.app_context():
#     db = LocalProxy(get_db)
#
# def query_db(query, args=(), one=False):
#     cur = db.execute(query, args)
#     rv = cur.fetchall()
#     cur.close()
#     return (rv[0] if rv else None) if one else rv
###########################################################################

# Jinja extensions and filters
# app.jinja_env.add_extension('jinja2.ext.do')
# app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# _paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')


# @app.template_filter()
# @evalcontextfilter
# def nl2br(eval_ctx, value):
#     result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', '<br>\n')
#                           for p in _paragraph_re.split(escape(value)))
#     if eval_ctx.autoescape:
#         result = Markup(result)
#     return result


# @app.before_request
# def make_session_permanent():
#     # Set to 'True' so that flask session does not expire after closing the browser (default is False)
#     session.permanent = True
#     # Set session timeout after period of inactivity (default is 31 days)
#     app.permanent_session_lifetime = timedelta(minutes=30)


def register_blueprints(app):
    from .views import BG_data
    app.register_blueprint(BG_data)

register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)
