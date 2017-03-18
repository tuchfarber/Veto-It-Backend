from bottle import route, run, get, post, request, response, hook
import couchdb

couch = couchdb.Server("http://couchdb_01:5984")

if 'vetoit' in couch:
    db = couch['vetoit']
else:
    db = couch.create('vetoit')

@hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'

@post('/vetoit/create')
def create():
    body = request.json
    data = {"gps":body["gps"],"init_km":body["init_km"],"del_ids":body["del_ids"]}
    (d_id, d_rev) = db.save(data)
    return {"d_id":d_id}

@get('/vetoit/retrieve/<d_id>')
def retrieve(d_id):
    if d_id in db:
        record = db[d_id]
        data = {"gps":record["gps"],"init_km":record["init_km"],"del_ids":record["del_ids"]}
    else:
        data = {"error":"Document does not exist"}
    return data