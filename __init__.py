from flask import Flask, render_template, request, jsonify
import os
import urllib
import urllib3
import simplejson
import json
import time


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
        start_q = time.time()
        keyword = request.args['keyword']
        category = request.args['category']
        if 'start_result' in request.args:
            start_result = request.args['start_result']
        else:
            start_result = 0
        if category == 'Tất cả thể loại':
            category = "*"
        http = urllib3.PoolManager()
        url_query = "http://0.0.0.0:8983/solr/vnexpress/select?hl.fl=content&hl=on&q=content:{} and category:{}&wt=json&start={}".format(keyword, category, start_result)
        r = http.request('GET', url_query)
        response = r.data.decode('utf-8')
        response = json.loads(response, encoding='utf-8')
        query_time = round(time.time() - start_q, 3)
        error ='error' in response

        if not error:
            n_found = response['response']['numFound']
            start_result = response['response']['start']
            docs = response['response']['docs']
            hl = response['highlighting']
            # return jsonify(hl)
            return render_template('result.html', n_found=n_found, query_time=query_time, start_result=start_result,
                                   docs=docs, hl=hl, keyword=keyword, category=category)
        else:
            return render_template('result.html', error=True, keyword=keyword, category=category)

    @app.route('/result')
    def result():
        return render_template('result.html')

    return app
