from flask import Flask, request
import urllib.request, json
from json2html import *

# creating the flask app
app = Flask(__name__)
# load the data
with urllib.request.urlopen("https://api.github.com/repos/walmartlabs/thorax/issues") as url:
    data = json.loads(url.read().decode())

# home screen
@app.route('/')
def hello_world():
    return issues()

# view issues
# print 10 rows from start number. use as /issues?start=12
@app.route('/issues')
def issues(start=0):
    l = request.args.get('start')
    if l:
        try:
            start = int(l)
        except:
            return "<h1>An error occurred while parsing start number</h1>"
    out = ""
    count = 0
    for issue in data[start:start + 10]:
        out += '<a href="/view?id={}"><H1>{}</H1></a><p>{}<br>{}</p><hr>'.format(start + count, issue['title'],
                                                                                 issue['id'], issue['state'])
        count += 1
    # no issues found
    if count == 0:
        out += '<h1>No issues found</h1><a href="/issues?start=0">Go home</a><hr>'
    # pagination
    # back = None
    if start > 10:
        back = start - 10
    elif start <= 10:
        back = 0
    next = start + 10
    out += '<a href="/issues?start={}">Back</a>&nbsp&nbsp&nbsp&nbsp<a href="/issues?start={}">Next</a>'.format(back,next)
    return out

# view issue in detail. use as /view?id=2
@app.route('/view')
def view():
    try:
        id = int(request.args.get('id'))
    except:
        return "<h1>An error occurred while parsing ID</h1>"
    if id > len(data):
        return "<h1>ID out of bound!</h1>"
    out = json2html.convert(json=data[id])
    return out


if __name__ == '__main__':
    app.run()
