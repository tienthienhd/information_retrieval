from flask import Flask, render_template, request
import os
import urllib
import urllib3
import simplejson
import json


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/search')
    def search():
        keyword = request.args['keyword']
        category = request.args['category']
        if category == 'Tất cả thể loại':
            category = "*"
        http = urllib3.PoolManager()
        url_query = "http://0.0.0.0:8983/solr/vnexpress/select?hl.fl=content&hl=on&q=content:{} and category:{}&wt=json".format(keyword, category)
        r = http.request('GET', url_query)
        response = r.data.decode('utf-8')
        response = json.loads(response, encoding='utf-8')

        return render_template('result.html', response=response)

    @app.route('/result')
    def result():
        return render_template('result.html')

    return app
