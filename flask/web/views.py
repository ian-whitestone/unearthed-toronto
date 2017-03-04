from flask import flash, Blueprint, request, redirect, render_template, url_for, jsonify, Markup, send_from_directory, Response, make_response
from flask.views import MethodView
from flask_login import LoginManager, UserMixin, login_required, current_user
from datetime import datetime, timedelta, date
import time
import json
from werkzeug.exceptions import NotFound
import subprocess
import shlex
import os
from werkzeug.utils import secure_filename

from . import app, allowed_file
# from . import query_db, db
from .login import login_manager  # THIS IS NEEDED
import database_operations as dbo


BG_data = Blueprint('BG_data', __name__, template_folder='templates')
ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))


class HomePage(MethodView):

    def get(self):
        return render_template('home.html')


class MineData(MethodView):
    decorators = [login_required]

    def get(self, report_id=None):
        if report_id:
            report = "data/%s.html" % report_id
        else:
            report = "data/report_full.html"
        url = url_for('static', filename=report)
        return render_template('mine_data.html', url=url)


class UploadData(MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('upload_data.html')


BG_data.add_url_rule('/', view_func=HomePage.as_view('home'))
BG_data.add_url_rule('/mines/', view_func=MineData.as_view('MineData'))
BG_data.add_url_rule('/mines/<report_id>/', view_func=MineData.as_view('CustomReport'))
BG_data.add_url_rule('/upload/', view_func=UploadData.as_view('UploadData'))


@app.route('/upload_file/', methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        ff = f.filename
        print('ff', f.filename)

        filename = "{name}_{time}".format(
            time=datetime.now().strftime("%Y%m%d-%H%M%S"), name=ff)
        print('filename', filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            f.save(filepath)
            print('uploaded to', filepath)
            # if filename.lower().startswith('data'):
            #     data_import.main(filepath)
            # elif filename.lower().startswith('survey'):
            #     import_survey.import_data(filepath)
            # print('data loaded successfully')
            # query = 'SELECT * FROM data'
            # title = 'Annual Report'
            # output_path = 'web/static/data/report_full.html'
            # render_call = "rmarkdown::render(\"report.Rmd\", params=list(query=\"%s\", title=\"%s\"), output_file = \"%s\")" % (
            #     query, title, output_path)
            # subprocess.call(['Rscript', '-e', render_call])
            return render_template('upload_success.html', ff=ff)
        except Exception as e:
            flash(Markup("Uh oh! Something went wrong. Please check your inputs again or contact an Admin.<br>"
                         "<b>{error}:</b> {msg}".format(error=type(e).__name__, msg=str(e))), 'danger')
            return redirect('/')
    else:
        return redirect(url_for('BG_data.UploadData'))


@app.route('/generate_report/')
@login_required
def generate_report():
    rpt = request.args.get('rpt')
    if rpt == "All":
        return redirect('/mines/')
    else:
        try:
            # query stuff
            url = '/mines/report_%s' % rpt
            return jsonify(result='Success', report=url)
        except Exception as e:
            flash(Markup("Uh oh! Something went wrong. Please check your inputs again or contact an Admin.<br>"
                         "<b>{error}:</b> {msg}".format(error=type(e).__name__, msg=str(e))), 'danger')
            return jsonify(result='Failed')

def construct_feature(lon, lat, properties):
    feature = {'type': 'Feature',
                'geometry': {
                    'type': 'Point',
                    'coordinates': [lon, lat]
                },
                'properties': properties}
    return feature

@app.route('/mines_api')
@login_required
def mine_api():
    conn = dbo.db_connect()

    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    data = dbo.select_query(conn, 
    """SELECT * FROM mines 
    WHERE geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326) limit 500""" 
    %(minlng, minlat, maxlng, maxlat))

    features = []
    for mine in data:
        features.append(construct_feature(mine[6], mine[5], dict(name=mine[1], owner=mine[2], stage=mine[3], activity=mine[4])))
    return jsonify(type='FeatureCollection', features=features)
    


@app.route('/test')
def test():
    return render_template('leaflet.html')