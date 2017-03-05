from flask import flash, Blueprint, request, redirect, render_template, url_for, jsonify, Markup, send_from_directory, Response, make_response
from flask.views import MethodView
from flask_login import LoginManager, UserMixin, login_required, current_user
from datetime import datetime, timedelta, date
import time
import json
from werkzeug.exceptions import NotFound
import subprocess
import requests
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
        info_found = True
        if info_found:
            info = {
                    "mine_id": "123",
                    "collapse_id": "collapse_123",
                    "name": "Mine 1",
                    "articles": [
                        {
                            "type": "news",
                            "title": "Exciting news",
                            "url": "https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q=barrick+gold",
                            "description": "Lorem ipsum dolor sit amet, ei quem noluisse inciderint eum, sed at maiorum dissentias. Ut pri graece euismod saperet, no mea option forensibus. Mei no vidit brute dissentiunt. Patrioque molestiae eum ex, est stet dolore nullam an. No vel graeci latine pertinacia, vim dolor splendide in, per fabulas accusata no. Ex vel harum omnium. At aeque disputationi pri. Feugiat epicuri ut nec. Sea no scripta bonorum fabulas, his ei mutat vitae. Ea pro iriure feugiat mnesarchum, quodsi audire eu quo. Labore constituam an sea. Has te nonumy eripuit, vero clita nostrud eu eos, illum dicta persequeris ei mel.",
                            "thumbnail": "https://si.wsj.net/public/resources/images/ON-BY988_gold_M_20170117160546.jpg",
                            "source": "mining.com",
                            "date": "Jan 31, 2017"
                        },
                        {
                            "type": "academic",
                            "title": "Gold mining industry",
                            "author": "Jane Smith",
                            "url": "https://scholar.google.com/scholar?hl=en&q=gold+mining+industry",
                            "description": "Vis id justo elitr pericula, cu sea dicta officiis. Omnis facer possit nec te, eos no sint scripta pericula. Admodum nominavi an his. Ut mea dicat consul, dicit mandamus an per. Has wisi novum iudicabit an, eu mundi malorum sed, mea no equidem detraxit intellegebat.",
                            "source": "academia.edu",
                            "date": "Jan 15, 2017",
                            "cited_by": "64"
                        },
                        {
                            "type": "search",
                            "title": "New findings in gold mining",
                            "url": "https://www.wsj.com/",
                            "description": "Ea est placerat phaedrum, inani dolores concludaturque vix ne, has eu graece mandamus. Et mel dicta veritus, no dolore consetetur eos. ",
                            "date": "Feb 20, 2017"
                        }
                    ]
                }
        else:
            info = None
        return render_template('home.html', info=info)


class SplashPage(MethodView):
    def get(self):
        return render_template('splash.html')


class Watchlist(MethodView):
    decorators = [login_required]

    def get(self):
        wl = True
        if wl:
            watchlist = [
                {
                    "mine_id": "68050",
                    "collapse_id": "collapse_68050",
                    "name": "Coffee Dome",
                    "articles": [
                        {
                            "type": "news",
                            "title": "Forest Service OKs Big Springs Mine project",
                            "url": "http://elkodaily.com/mining/forest-service-oks-big-springs-mine-project/article_cc309b22-0280-5673-b2bf-01f6dce9e9c9.html",
                            "description": "Anova Metals USA LLC to begin mining for gold at the former Big Springs Mine site, which was previously mined between 1987 and 1993.",
                            "thumbnail": "https://si.wsj.net/public/resources/images/ON-BY988_gold_M_20170117160546.jpg",
                            "source": "Elko Daily Free Press",
                            "date": "Mar 3, 2017"
                        },
                        {
                            "type": "academic",
                            "title": "Gold mining industry",
                            "author": "G. Wilson",
                            "url": "http://onlinelibrary.wiley.com/doi/10.1111/j.1470-9856.2011.00529.x/full",
                            "description": "Stope backfilling in gold mines uses the coarser cyclone fraction of the gold tailings. The disposal of the overflow from the cyclones, which is finer and of higher moisture content than normal gold tailings, presents some problems.",
                            "source": "academia.edu",
                            "date": "Jan 15, 2015",
                            "cited_by": "64"
                        },
                        {
                            "type": "search",
                            "title": "Bewitched By a Giant Green Rock",
                            "url": "https://www.wired.com/2017/03/curse-bahia-emerald-giant-green-rock-wreaks-havoc-ruins-lives/",
                            "description": "Diamonds are a product like gold or crude oil: rational, conservative. Emeralds are Turkish rugs. When you buy one you .... The Gem of Tanzania, a 10,000-carat ruby, was once valued at 11 million British pounds, but that appraisal turned out to be a...",
                            "source": "WIRED",
                            "date": "Mar 2, 2017"
                        }
                    ]
                },
                {
                    "mine_id": "24433",
                    "collapse_id": "collapse_24433",
                    "name": "Golden Summit",
                    "articles": [
                        {
                            "type": "news",
                            "title": "St. Augustine Gold & Copper Provides Update on MPSA",
                            "url": "http://www.montrealgazette.com/business/cnw/release.html?rkey=20170220C8472&filter=5611",
                            "description": "The King-king Copper-Gold Project is located in Compostela Valley in the Philippines, and is expected to recover 3.16 billion pounds (1.43 million tonnes) of copper and 5.43 million troy ounces (169,000 kilograms) of gold over its 25 year mine and...",
                            "thumbnail": "https://si.wsj.net/public/resources/images/ON-BY988_gold_M_20170117160546.jpg",
                            "source": "Montreal Gazette",
                            "date": "Feb 20, 2017"
                        },
                        {
                            "type": "search",
                            "title": "New findings in gold mining",
                            "url": "https://www.wsj.com/",
                            "description": "Over the past two decades, the gold mining industry has increased its activity in Latin America. Growing contestation and conflict around gold mining projects have accompanied this shift.",
                            "date": "Feb 20, 2017"
                        }
                    ]
                },
                {
                    "mine_id": "49920",
                    "collapse_id": "collapse_49920",
                    "name": "West Pogo",
                    "articles": []
                }

            ]
        else:
            watchlist = None
        return render_template('watchlist.html', watchlist=watchlist)


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


class News(MethodView):
    decorators = [login_required]

    def get(self):
        conn = dbo.db_connect()
        articles = dbo.select_query(conn,
                                         """select title, link, description, source, date, a.ticker, name
                                             from company_news as a
                                             join companies as b
                                             on a.ticker = b.ticker
                                             order by a.date desc""")

        news_list = []
        for article in articles:
            news_list.append({"title": article[0],
                             "link": article[1],
                             "description": article[2],
                             "source": article[3],
                             "date": article[4],
                             "ticker": article[5],
                             "company": article[6]})

        return render_template('news.html', news_list=news_list)

BG_data.add_url_rule('/', view_func=SplashPage.as_view('home'))
BG_data.add_url_rule('/explore', view_func=HomePage.as_view('Explore'))
BG_data.add_url_rule('/watchlist', view_func=Watchlist.as_view('Watchlist'))
BG_data.add_url_rule('/mines/', view_func=MineData.as_view('MineData'))
BG_data.add_url_rule('/mines/<report_id>/', view_func=MineData.as_view('CustomReport'))
BG_data.add_url_rule('/upload/', view_func=UploadData.as_view('UploadData'))
BG_data.add_url_rule('/news', view_func=News.as_view('News'))


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
def mine_api():
    conn = dbo.db_connect()

    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    data = dbo.select_query(conn,
    """SELECT a.mine_id, mine_name, owners,
        development_stage, activity_status,
        lat, lon,
        coalesce(b.mine_id, 0) fav FROM mines a left join favs b on a.mine_id = b.mine_id
    WHERE geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326) limit 500"""
    %(minlng, minlat, maxlng, maxlat))

    features = []
    for mine in data:
        features.append(construct_feature(mine[6], mine[5],
            dict(id=mine[0],
                name=mine[1],
                owner=mine[2],
                stage=mine[3],
                activity=mine[4],
                fav=mine[7])))
    return jsonify(type='FeatureCollection', features=features)

@app.route('/claims_api')
def claims_api():
    conn = dbo.db_connect()

    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    data = dbo.select_query(conn,
        """select a.mtrs, ST_AsGeoJSON(ST_ForceRHR(poly::geometry)) geom
            ,sum(case when claim_type LIKE 'LODE%%' THEN claim_count else 0 END) lode
            ,sum(case when claim_type LIKE 'MILL%%' THEN claim_count else 0 END) mill
            ,sum(case when claim_type LIKE 'TUNNEL%%' THEN claim_count else 0 END) tunnel
            ,sum(case when claim_type LIKE 'PLACER%%' THEN claim_count else 0 END) placer
            ,sum(claim_count)
        from claims_geo a join claims_meta b on a.mtrs = b.mtrs
        where poly && ST_MakeEnvelope(%s, %s, %s, %s, 4326)
        group by 1, 2 having sum(claim_count) > 0"""
    %(minlng, minlat, maxlng, maxlat))

    claims = []
    for claim in data:
        claim_data = dict(geometry=eval(claim[1]), type='Feature')
        claim_data['properties'] = dict(lode=claim[2],
                                        mill=claim[3],
                                        tunnel=claim[4],
                                        placer=claim[5],
                                        total=claim[6])

        claims.append(claim_data)

    return jsonify(type='FeatureCollection', features=claims)

@app.route('/update_fav', methods=['GET','PUT'])
def update_fav():
    mine_id = request.args.get('id')
    conn = dbo.db_connect()
    fav = dbo.select_query(conn,
    "SELECT * FROM favs where mine_id = %s" %mine_id)
    if not fav:
        dbo.execute_query(conn,
            "INSERT INTO favs VALUES (%s)" %mine_id)
        return jsonify(status="Added Favorite")
    else:
        dbo.execute_query(conn,
            "DELETE FROM favs WHERE mine_id = %s" %mine_id)
        return jsonify(status="Deleted Favorite")

@app.route('/is_fav', methods=['GET'])
def is_fav():
    mine_id = request.args.get('id')
    conn = dbo.db_connect()
    fav = dbo.select_query(conn,
    "SELECT * FROM favs where mine_id = %s" %mine_id)
    if fav:
        return jsonify(status=1)
    else:
        return jsonify(status=0)

@app.route('/faults_api')
def faults_api():
    conn = dbo.db_connect()

    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    query = """select name, ftype, cast(cast(length as decimal(6,1)) as varchar) , sliprate, age, ST_AsGeoJSON(fault_str::geometry)
        from faults where length(fault_str) > 50
        and fault_str::geometry && ST_MakeEnvelope(%s, %s, %s, %s, 4326)""" %(minlng, minlat, maxlng, maxlat)

    data = dbo.select_query(conn, query)
    print(data)

    faults = []
    for fault in data:
        fault_line = dict(type='Feature', geometry=eval(fault[5]))
        fault_line['properties'] = dict(name=fault[0],
                                        ftype=fault[1],
                                        length=fault[2],
                                        sliprate=fault[3],
                                        age=fault[4])
        faults.append(fault_line)

    return jsonify(type='FeatureCollection', features=faults)

@app.route('/get_news', methods=['GET'])
def get_news():
    mine_id = request.args.get('id')
    conn = dbo.db_connect()
    google_data = dbo.select_query(conn,
        "select title, link, description, source, date, 'google' from google_news where mine_id = %s limit 5" %mine_id)
    # # scholar_data = dbo.select_query(conn,
    #     """select title, link, author, cited_by, NULL from scholar_news where mine_id = %s""" %mine_id)
    # data = google_data.append(scholar_data)
    # google_data = [("title1", "http://www.google.ca", 'hi', 'me', None),
    #                 ("title2", "http://www.google.ca", 'hi', 'me', None),
    #                 ("title3", "http://www.google.ca", 'hi', 'me', None),
    #                 ("title4", "http://www.google.ca", 'hi', 'me', None),
    #                 ("title5", "http://www.google.ca", 'hi', 'me', None)]
    if len(google_data) == 0:
        google_data = dbo.select_query(conn,
            "select title, link, description, source, date, 'google' from google_news where mine_id = 24439 limit 5")

    features = []
    for article in google_data:
        features.append({"title":article[0],
                            "link":article[1],
                            "description":article[2],
                            "source":article[3],
                            "date":article[4],
                            "type":article[5]})

    return jsonify(features=features)

@app.route('/get_news_in_area', methods=['GET'])
def get_news_in_area():
    minlat = request.args.get('minlat')
    minlng = request.args.get('minlng')
    maxlat = request.args.get('maxlat')
    maxlng = request.args.get('maxlng')

    conn = dbo.db_connect()
    google_data = dbo.select_query(conn,
        """select title, link, description, source, date
            from google_news a join mines b on a.mine_id = b.mine_id
            where geom @ ST_MakeEnvelope(%s, %s, %s, %s, 4326) limit 5"""
            %(minlng, minlat, maxlng, maxlat))

    if len(google_data) == 0:
        google_data = dbo.select_query(conn,
            "select title, link, description, source, date from google_news where mine_id = 24439 limit 5")

    features = []
    for article in google_data:
        features.append({"title":article[0],
                            "link":article[1],
                            "description":article[2],
                            "source":article[3],
                            "date":article[4]})

    return jsonify(features=features)


@app.route('/usgs_api')
def getUSGS():
    
    lon = request.args.get('lon')
    lat = request.args.get('lat')

    BASE_URL = "https://mrdata.usgs.gov/general/near-point.php?x={0}&y={1}&d=0.01"

    FIELDS_MAP = {
        'USGS Publications': 'pubs',
        'Estimates of undiscovered mineral resources': 'nmra'
    }

    url = BASE_URL.format(lon, lat)
    print (url)
    r = requests.get(url)
    d = json.loads(r.text)
    data = {d['title']:d for d in d['dataset']}

    cleaned_data = {}
    for k, v in FIELDS_MAP.items():
        records = data.get(k, None)
        if records:
            cleaned_data[v] = records['record_list']
    return jsonify(data=cleaned_data)
