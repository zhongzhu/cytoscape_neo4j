# coding=utf-8
from flask import Flask, jsonify
# from flask.ext.jsonpify import jsonify
from py2neo import Graph

app = Flask(__name__)
graph = Graph()

def buildNodes(nodeRecord):
    data = {"id": str(nodeRecord.n._id), "type": next(iter(nodeRecord.n.labels))}
    data.update(nodeRecord.n.properties)

    return {"data": data}

def buildEdges(relationRecord):
    data = {"source": str(relationRecord.r.start_node._id), 
            "target": str(relationRecord.r.end_node._id),
            "relationship": relationRecord.r.rel.type}

    return {"data": data}

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/graph')
def get_graph():
    nodes = map(buildNodes, graph.cypher.execute('MATCH n return n'))
    edges = map(buildEdges, graph.cypher.execute('MATCH ()-[r]->() RETURN r'))  

    return jsonify(elements = {"nodes": nodes, "edges": edges})    

if __name__ == '__main__':
    app.debug = True
    app.run()