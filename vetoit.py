from bottle import route, run, get, post, request
import couchdb

couch = couchdb.Server()

if 'vetoit' in couch:
    db = couch['vetoit']
else:
    db = couch.create('vetoit')

@post('/create')
def create():
    body = request.json
    data = {"gps":body["gps"],"init_km":body["init_km"],"del_ids":body["del_ids"]}
    (d_id, d_rev) = db.save(data)
    return {"d_id":d_id}

@get('/retrieve/<d_id>')
def retrieve(d_id):
    record = db[d_id]
    data = {"gps":record["gps"],"init_km":record["init_km"],"del_ids":record["del_ids"]}
    return data

run(host="0.0.0.0",port="40404")