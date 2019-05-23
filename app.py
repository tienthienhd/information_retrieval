from flask import Flask, render_template, request
import os
import urllib3
import requests
import time
import json
import urllib
from underthesea import word_tokenize

from flask_paginate import Pagination, get_page_args

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def query(keyword, offset, per_page):
    start_time = time.time()
    url_query = "http://0.0.0.0:8983/solr/vnexpress/select?defType=dismax&&qf=title^0.3+content^0.5+category^0.2&hl.fl=content&hl.fragsize=400&hl=on&hl.simple.post=<%2Fb>&hl.simple.pre=<b>&wt=json&start={}&rows={}&q={}".format(
        offset, per_page, keyword)

    response = requests.get(
        url=url_query,
        headers={
            'Content-type': 'application/json',
            'Accept': 'application/json',
        },
    )

    response = json.loads(response.content, encoding='utf-8')
    query_time = round(time.time() - start_time, 3)

    error = 'error' in response
    if not error:
        n_found = response['response']['numFound']
        # start_result = response['response']['start']
        docs = response['response']['docs']
        hl = response['highlighting']
        return query_time, n_found, docs, hl
    return error

@app.route('/search')
def search():
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    keyword = request.args['keyword']
    keyword = word_tokenize(keyword, format='text')

    results = query(keyword, offset, per_page)

    if results == True:
        print('error query')
        return render_template('result.html', error=True)

    query_time, n_found, docs, hl = results

    pagination = Pagination(page=page, per_page=per_page, total=n_found,
                            css_framework='bootstrap4')

    return render_template('result.html', docs=docs, hl=hl, n_found=n_found, query_time=query_time,
                           keyword=keyword,
                           page=page, per_page=per_page, pagination=pagination)



@app.route('/advanced_search')
def advanced_seach():
    return render_template('advanced_search.html')


def advanced_query(title, category, content, offset, per_page):
    print(title, category, content)
    if len(title) <= 1:
        title = "*"
    if category == 'Tất cả thể loại':
        category = "*"
    if len(content) <= 1:
        content = "*"
    url = "http://0.0.0.0:8983/solr/vnexpress/select"
    params = "?qf=title^0.3+content^0.5+category^0.2&hl.fl=content&hl.fragsize=400&hl=on&hl.requireFieldMatch=true&hl.simple.post=</b>&hl.simple.pre=<b>&wt=json&start={}&rows={}&".format(offset, per_page)
    input = "q=content:{} AND title:{} AND category:{}".format(content, title, category)
    start_time = time.time()
    url_query = url + params + input
    print(url_query)
    response = requests.get(
        url=url_query,
        headers={
            'Content-type': 'application/json',
            'Accept': 'application/json',
        },
    )
    response = json.loads(response.content, encoding='utf-8')
    query_time = round(time.time() - start_time, 3)

    error = 'error' in response
    if not error:
        n_found = response['response']['numFound']
        # start_result = response['response']['start']
        docs = response['response']['docs']
        if n_found > 0:
            hl = response['highlighting']
            return query_time, n_found, docs, hl

        return True
    return error

@app.route('/search_ad')
def search_ad():
    title = request.args['title']
    title = word_tokenize(title, format='text')
    category = request.args['category']
    content = request.args['content']
    content = word_tokenize(content, format='text')

    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    results = advanced_query(title, category, content, offset, per_page)

    keyword = "title:" + title + ", category:" + category + ", content:" + content

    if results == True:
        return render_template('result.html', error=True, keyword=keyword)
    query_time, n_found, docs, hl = results

    pagination = Pagination(page=page, per_page=per_page, total=n_found,
                            css_framework='bootstrap4')

    return render_template('result.html', docs=docs, hl=hl, n_found=n_found, query_time=query_time,
                           keyword=keyword,
                           page=page, per_page=per_page, pagination=pagination)
    return content

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)