from bottle import route, run, get, post, request
import couchdb

couch = couchdb.Server("http://couchdb_01:5984")

if 'vetoit' in couch:
    db = couch['vetoit']
else:
    db = couch.create('vetoit')

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
        data = {"status":"Error", "status_text": "Document does not exist"}
    return data

@post('/vetoit/veto/<d_id>')
def veto(d_id):
    body = request.json
    if d_id in db:
        record = db[d_id]
        unique_dels = set(body["del_ids"] + record["del_ids"])
        record["del_ids"] = unique_dels
        db[record['id']] = record
        return {"status":"Success", "status_text": "Document successfully updated"}
    else:
        return {"status":"Error", "status_text": "Document does not exist"}