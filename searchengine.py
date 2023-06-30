from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os

os.chdir('/home/fswithes8')
password = os.getenv('ELASTIC_PASSWORD')
print(password)
app = Flask(__name__)
es = Elasticsearch('https://elastic:W3lcomeAA**@localhost:9200', verify_certs=False, basic_auth=("elastic","W3lcomeAA**") )


@app.route('/')
def home():
    return render_template('search.html')

@app.route('/search/results', methods=['GET','POST'])
def request_search():
    search_term = request.form['input']
    res = es.search(
    index='idx',
    body={
    "query" : {"match": {"content": search_term}},
    "highlight" : {"pre_tags" : ['<b>'] , "post_tags" : ["</b>"], "fields" : {"content":{}}}})
    res['ST']=search_term

    for hit in res['hits']['hits']:
        hit['good_summary']='….'.join(hit['highlight']['content'][1:])
        hit['virtual'] = hit['_source']['path']['virtual']
        tokens = hit['virtual'].split("/")
        hit['year'] = tokens[1]
        hit['case'] = tokens[2]

    return render_template('results.html', res=res)

if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)

