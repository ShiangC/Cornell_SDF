from flask import Flask, render_template, url_for, request, redirect, Response, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from Decision_Model import tradespace_explore
from Rhodium_Model.trade_speace_rhodium import TradeSpaceRhodium
import subprocess
import time
import csv

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Outputs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return '<%r>' % self.id


priceVector = {
                'yield': 100,
                'electricity': 10,
                'water': 5,
                'pesticides': 50,
                'labor': 300
            }
ts = None
r_model = TradeSpaceRhodium()
paretoSet = None
model = None
optimalSet = None
eval_res = None

numOfUsers = None
latitude = None
sampEn = None
rainfall = None
cost_range = None
perf_range = None
risk_range = None


results = ""


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/generate', methods=['GET'])
def generate_ts():
    global ts
    if ts is None:
        ts = tradespace_explore.Tradespace(0, priceVector)
    res = make_response("Generate TS Success")
    res.status = '200'
    res.headers['ts_len'] = len(ts.tradeSpace)
    return res


@app.route('/pareto', methods=['GET'])
def pareto():
    global paretoSet
    if paretoSet is None:
        paretoSet = ts.calcPareto()
        ts.plotTS(paretoSet)
    res = make_response("Calc Pareto Success")
    res.status = '200'
    res.headers['ps_len'] = len(paretoSet)
    return res


@app.route('/update_model', methods=['POST', 'GET'])
def update_model():
    global model
    global numOfUsers
    global latitude
    global sampEn
    global rainfall
    global cost_range
    global perf_range
    global risk_range
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        numOfUsers = int(data['numOfUsers'])
        latitude = int(data['latitude'])
        sampEn = float(data['sampEn'])
        rainfall = float(data['rainfall'])
        cost_range = data['cost_range']
        perf_range = data['perf_range']
        risk_range = data['risk_range']
        model = r_model.setupModel(r_model.farm_approach2, paretoSet, numOfUsers, latitude,
                                   sampEn, rainfall, 1, cost_range, perf_range, risk_range)
    res = make_response("Update Model Success")
    res.status = '200'
    return res


@app.route('/optimize')
def optimize():
    global optimalSet
    optimalSet = r_model.optimizeModel(model)
    res = make_response("Optimize Success")
    res.status = '200'
    res.headers['ps_len'] = len(optimalSet)
    return res


@app.route('/policy_eval')
def policy_eval():
    global eval_res
    eval_res = r_model.policyEval(model, optimalSet['node'], numOfUsers, latitude, sampEn, rainfall, 1)
    res = make_response("Eval Success")
    res.status = '200'
    return res

@app.route('/sa')
def sensitivity_analysis():
    r_model.SD(eval_res, model, perf_range, cost_range, risk_range)
    # r_model.SA(model, optimalSet['node'], numOfUsers, latitude, sampEn, rainfall, 1)
    res = make_response("SA Success")
    res.status = '200'
    return res




if __name__ == "__main__":
    app.run(debug=True)
