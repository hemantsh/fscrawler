from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
import os

os.chdir('/Users/hemant/projects/FSElastic')
app = Flask(__name__)
es = Elasticsearch('https://localhost:9200')


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
    "highlight" : {"pre_tags" : ['<b>'] , "post_tags" : ["</b>"], "fields" : {"content":{}}
                  }
    }
    )
    
    res['ST']=search_term

    for hit in res['hits']['hits']:
        hit['good_summary']='….'.join(hit['highlight']['content'][1:])
        
    return render_template('results.html', res=res)
                        
if __name__ == '__main__':
    app.run('127.0.0.1', debug=True)
