import sys  
import os
sys.path.insert(0, '')
import agent as ai

from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

#Members API Route

@app.route("/members", methods = ['GET', 'POST'])
def members():
    ai.reset_knowledge()
    ai.output_memery={}
    ai.servicelist=[]
    value1=ai.OperatingTask ('task10','pkson.csv',['pipeline'],'medical','','MLmodel_classification')

    # taskName = str(request.form.get("taskName"))
    # path = request.args.get('path', None)
    # value2=ai.OperatingTask (str(name),str(path),['pipeline'],'medical','','MLmodel_classification')

    return {"members": [str(value1[0]), "", ""]}

@app.route('/result', methods = ['POST'])
def result():
    name=request.form['name']
    path=request.form['path']
    return {"members": [str(name), str(path), ""]}
    
if __name__ == "__main__":
    app.run(debug=True)


