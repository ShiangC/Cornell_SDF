from rhodium import *
from Decision_Model.decision_model import Decision
from Decision_Model.tradespace_explore import Tradespace
from scipy.optimize import brentq as root
from j3 import J3
import numpy as np
import itertools
import csv
import plotly.express as px


class TradeSpaceRhodium():

    def farm_approach2(self, node, numOfUsers, latitude, crop_type, sampEn, rainfall):
        performance = node['perf']
        risk = node['risk']
        policy = node['policy']
        data_storage_risk = 0
        maintenance_cost = 0
        hardware_cost = 0

        for decision in policy:
            d_perf = decision.getPerf()
            d_cost = decision.getCost()
            d_risk = decision.getRisk()
            if decision.description == 'User Interface' or decision.description == 'Data Collection':
                performance -= d_perf * (latitude / 1000) # Account for the latitude effects
            if decision.description == 'ML Model':
                performance = performance - d_perf + (-1 / 9 * (sampEn ** 2) + 1) * d_perf # Account for the climate complexity effects
                risk = risk - d_risk + (-1 / 9 * (sampEn ** 2) + 1) * d_risk
            if decision.description == 'iOT Devices':
                hardware_cost += d_cost
            if decision.description == 'User Interface' or decision.description == 'Data Storage':
                maintenance_cost += d_cost
                if decision.description == 'Data Storage':
                    data_storage_risk += d_risk

        maintenance_cost = hardware_cost + (maintenance_cost / numOfUsers)
        cost = maintenance_cost + hardware_cost*numOfUsers
        # predicted_yield = regression_rainfall_yield(crop_type, rainfall)
        risk += data_storage_risk
        policy_names = node['policy_names']

        return performance, cost, risk, node, policy_names


    # Maps crop type to a linear regression between rainfall and crop yield
    def regression_rainfall_yield(self, crop_type, rainfall):
        if crop_type is 1: #Linear regression for Wheat
            return 0.0000037434 * rainfall - 0.01301198
        if crop_type is 2: #Linear regression for Potato
            return -0.00029371 * rainfall + 0.81806965
        if crop_type is 3: #Linear regression for Grape
            return 0.07286135 * rainfall - 18.21006311


    # Setup the model
    def setupModel(self, func, nodes, input_numOfUsers, input_latitude, input_sampleEn, input_rainFall, input_cropType):
        # Setting up Rhodium Model
        model = Model(func)
        model.parameters = [Parameter("node"),
                            Parameter("numOfUsers", default_value=input_numOfUsers),
                            Parameter("latitude", default_value=input_latitude),
                            Parameter("sampEn", default_value=input_sampleEn) ,
                            Parameter("rainfall", default_value=input_rainFall),
                            Parameter("crop_type", default_value=input_cropType)]

        model.responses = [Response("performance", Response.MAXIMIZE),
                           Response("cost", Response.MINIMIZE),
                           Response("risk", Response.MINIMIZE),
                           Response("node", Response.INFO),
                           Response("policy_names", Response.INFO)]
        model.constraints = []

        model.levers = [CategoricalLever("node", nodes)]

        model.uncertainties = [NormalUncertainty("numOfUsers", input_numOfUsers, 100),
                               NormalUncertainty("latitude", input_latitude, 3),
                               NormalUncertainty("sampEn", 2.68, 0.136),
                               NormalUncertainty("rainfall", 1302.775, 555.243)]
        return model


    # Optimization
    def optimizeModel(self, model):
        output = optimize(model, "NSGAII", 10000)
        print('\x1b[0;32;44m' + "Found", len(output), "optimal policies!" + '\x1b[0m')
        # fig = scatter3d(model, output, c="risk",
        #                 brush=[Brush("performance > 500"), Brush("performance <= 500")])
        output.as_dataframe(['performance', 'cost', 'risk', 'node', 'policy_names'])\
              .to_csv(r'../web_app/static/rhodium_optimize.csv')
        return output


    # Policy Evaluation
    def policyEval(self, model, nodes, numOfUsers, latitude, sampEn, rainfall, crop_type):
        print('\x1b[0;32;44m' + '************ Policy Evaluation ************' + '\x1b[0m')
        df = pd.DataFrame()
        SOWs = sample_lhs(model, 1000)

        for i in range(len(nodes)):
            sample = {"node": nodes[i], "numOfUsers": numOfUsers, "latitude": latitude, "sampEn": sampEn,
                      "rainfall": rainfall,
                      "crop_type": crop_type}
            results = evaluate(model, update(SOWs, sample))
            index = [i] * 1000
            results = results.as_dataframe(['performance', 'cost', 'risk', 'numOfUsers', 'latitude', 'sampEn', 'rainfall'])
            results['index'] = index
            df = df.append(results, ignore_index=True)

            # total = {'perf': 0, 'cost': 0, 'risk': 0}
            # for result in results:
            #     total['perf'] += result['performance']
            #     total['cost'] += result['cost']
            #     total['risk'] += result['risk']
            # average_result = {'avg_perf': [total['perf']/len(results)],
            #                   'avg_cost': [total['cost']/len(results)],
            #                   'avg_risk': [total['risk']/len(results)]}
            # avg_result = pd.DataFrame(average_result)
            # df = df.append(avg_result, ignore_index=True)

        df.to_csv(r'../results/rhodium_policy_eval.csv')
        fig = px.parallel_coordinates(df, color="index", labels={"performance": "performance",
                                                                      "cost": "cost", "risk": "risk",
                                                                      "numOfUsers": "numOfUsers", "sampEn": "sampEn", },
                                      color_continuous_scale=px.colors.diverging.Tealrose,
                                      color_continuous_midpoint=10)

        # fig = px.scatter(df, x="performance", y="cost", color="index",
        #                 size='risk', hover_data=['index'])
        fig.show()


        # J3(df)
        # h = plt.plot(df['performance'], df['cost'], df['risk'], '.b', markersize=8)
        # plt.show()
        # fig = scatter3d(model, df.values.tolist(), c="sampleEn",
        #                 brush=[Brush("performance > 450"), Brush("performance <= 450")])


    # Scenario Discovery
    def SD(self, results):
        print('\x1b[0;32;44m' + '************ Scenario Discovery using PRIM ************' + '\x1b[0m')
        classification = results.apply("'Effective' if performance > 450 else 'Ineffective'")
        p = Prim(results, classification, include=model.uncertainties.keys(), coi="Effective")
        box = p.find_box()
        # fig = box.show_tradeoff()
        # box.show_details()
        # plt.show()

    def SA(self, model, nodes, numOfUsers, latitude, sampEn, rainfall, crop_type):
        # Sensitivity Analysis
        print('\x1b[0;32;44m' + '************ Sensitivity Analysis ************' + '\x1b[0m')
        sample = {"node": nodes[0], "numOfUsers": numOfUsers, "latitude": latitude, "sampEn": sampEn, "rainfall": rainfall,
                  "crop_type": crop_type}
        result_s = sa(model, "performance", policy=sample, method="sobol", nsamples=1000)
        print(result_s)
        fig = result_s.plot()


    # def main():
    #     # Initialize Variables
    #     numOfUsers = 1000
    #     latitude = 45
    #     rainfall = 1302.775
    #     sampEn = 2.68
    #     crop_type = 1
    #     priceVector = {
    #         'yield': 100,
    #         'electricity': 10,
    #         'water': 5,
    #         'pesticides': 50,
    #         'labor': 300
    #     }
    #
    #     ts = Tradespace(0, priceVector)
    #
    #     # Tradespace Enumeration and calculate Pareto Fronts
    #     enum = ts.tradeSpace
    #     print('Number of Policies found: ' + str(len(enum)))
    #     nodes = ts.TS_nodes
    #     pareto_set = ts.calcPareto()  # the set of pareto policies
    #     ts.plotTS(pareto_set)
    #
    #     # Initialize model
    #     model = setupModel(farm_approach2, pareto_set, numOfUsers, latitude, sampEn, rainfall, crop_type)
    #
    #     # Optimization
    #     optimize_result = optimizeModel(model)
    #
    #     # Policy Evaluation
    #     policyEval(model, optimize_result['node'], numOfUsers, latitude, sampEn, rainfall, crop_type)
    #
    #     # Sensitivity Analysis
    #     # SA(model, pareto_set, numOfUsers, latitude, sampEn, rainfall, crop_type)
    #
