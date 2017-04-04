from bottle import route, run, get, post, request
import couchdb
import uuid
import time

couch = couchdb.Server("http://couchdb_01:5984")

if 'vetoit' in couch:
    db = couch['vetoit']
else:
    db = couch.create('vetoit')

@post('/vetoit/create')
def create():
    body = request.json
    d_key = str(uuid.uuid4())
    data = {"gps":body["gps"],"init_km":body["init_km"],"del_ids":body["del_ids"],"d_key":d_key, "expires":int(time.time()) + 3600}
    (d_id,_) = db.save(data)
    return {"d_id":d_id,"d_key":d_key}

@get('/vetoit/retrieve/<d_id>/<d_key>')
def retrieve(d_id,d_key):
    if d_id in db:
        record = db[d_id]
        if record["expires"] < int(time.time()):
            db.delete(record)
            return {"status":"Error", "status_text": "Item has expired"}
        if d_key == record["d_key"]:
            return {"gps":record["gps"],"init_km":record["init_km"],"del_ids":record["del_ids"]}
        else:
            return {"status":"Error", "status_text": "Provided key invalid"}
    else:
        return {"status":"Error", "status_text": "Document does not exist"}

@post('/vetoit/veto/<d_id>/<d_key>')
def veto(d_id,d_key):
    body = request.json
    if d_id in db:
        record = db[d_id]
        if record["expires"] < int(time.time()):
            db.delete(record)
            return {"status":"Error", "status_text": "Item has expired"}
        if d_key == record["d_key"]:
            unique_dels = set(body["del_ids"] + record["del_ids"])
            record["del_ids"] = unique_dels
            db[record["_id"]] = record
            return {"status":"Success", "status_text": "Document successfully updated"}
        else:
            return {"status":"Error", "status_text": "Provided key invalid"}
    else:
        return {"status":"Error", "status_text": "Document does not exist"}