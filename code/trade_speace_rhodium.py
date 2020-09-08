# from rhodium import *
from Decision_Model.decision_model import Decision
from Decision_Model.tradespace_explore import Tradespace
# from scipy.optimize import brentq as root
# from j3 import J3
# import numpy as np
# import itertools
# import csv

# plotting option
# %matplotlib inline
# sns.set()
# sns.set_style('darkgrid')


def farm_approach2(D1, D2, D3, D4, D5, D6, D7, D8, D9, D10,
                   tradeSpeace,
                   numOfUsers,
                   latitude,
                   crop_type,
                   sampEn=2.68,
                   rainfall=1302.775):
    policy = [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10]
    performance = 1

    # Account for latitude changes
    # decisions[5]['decisions'][policy[5]]['performance'] *= (1 - (latitude / 1000))
    # decisions[2]['decisions'][policy[2]]['performance'] *= (1 - (latitude / 1000))

    # Regional Climate complexity (sampEn) affects ML performance and risk
    # decisions[9]['decisions'][policy[9]]['performance'] *= (-1/9 * (sampEn ** 2) + 1)
    # decisions[9]['decisions'][policy[9]]['risk'] += (-1/9 * (sampEn ** 2) + 1)

    # Crop production predicted by linear regression given crop type
    # predicted_yield = regression_rainfall_yield(crop_type, rainfall)

    for i in range(9):
        performance *= decisions[i]['decisions'][policy[i]]['performance']
        if i is 2 or i is 5:
            performance *= (1 - (latitude / 1000))  # Account for the latitude effects
        elif i is 9:
            performance *= (-1 / 9 * (sampEn ** 2) + 1)  # Account for the climate complexity effects

    IoT_cost = decisions[1]['decisions'][D2]['cost']
    UI_cost = decisions[2]['decisions'][D3]['cost']
    DataStorage_cost = decisions[4]['decisions'][D5]['cost']

    ML_risk = decisions[9]['decisions'][D10]['risk']
    DataStorage_risk = decisions[4]['decisions'][D5]['risk']

    matainance_cost = IoT_cost + (UI_cost + DataStorage_cost) / numOfUsers
    hardware_cost = IoT_cost * numOfUsers

    cost = matainance_cost + hardware_cost
    risk = (ML_risk * (1 / 9 * (sampEn ** 2) + 1)) + DataStorage_risk

    # TENTATIVE; Needs to figure out how yield affects performance
    performance += predicted_yield

    return (performance, cost, risk)

# Setup the model
def setupModel(func, model):
    # Setting up Rhodium Model
    model = Model(farm_approach2)
    model.parameters = [Parameter("D1"),
                        Parameter("D2"),
                        Parameter("D3"),
                        Parameter("D4"),
                        Parameter("D5"),
                        Parameter("D6"),
                        Parameter("D7"),
                        Parameter("D8"),
                        Parameter("D9"),
                        Parameter("D10"),
                        Parameter("numOfUsers"),
                        Parameter("latitude"),
                        Parameter("sampEn"),
                        Parameter("rainfall"),
                        Parameter("crop_type")]

    model.responses = [Response("performance", Response.MAXIMIZE),
                       Response("cost", Response.MINIMIZE),
                       Response("risk", Response.MINIMIZE)]
    model.constraints = []

    model.levers = [IntegerLever("D1", 0, 6, 1),
                    IntegerLever("D2", 0, 2, 1),
                    IntegerLever("D3", 0, 6, 1),
                    IntegerLever("D4", 0, 2, 1),
                    IntegerLever("D5", 0, 1, 1),
                    IntegerLever("D6", 0, 6, 1),
                    IntegerLever("D7", 0, 2, 1),
                    IntegerLever("D8", 0, 6, 1),
                    IntegerLever("D9", 0, 2, 1),
                    IntegerLever("D10", 0, 2, 1)]


# Optimization
def optimizeModel(model):
    output = optimize(model, "NSGAII", 100)
    print('\x1b[0;32;44m' + "Found", len(output), "optimal policies!" + '\x1b[0m')
    print(output)
    output.as_dataframe(['performance', 'cost', 'risk']).to_csv(r'../results/pareto_policies.csv')


# Policy Evaluation
def policyEval(model):
    model.uncertainties = [NormalUncertainty("numOfUsers", input_numOfUsers, 100),
                           NormalUncertainty("latitude", input_latitude, 3),
                           NormalUncertainty("sampEn", 2.68, 0.136),
                           NormalUncertainty("rainfall", 1302.775, 555.243)]
    policy = {"D1": 4, "D2": 0, "D3": 3, "D4": 1, "D5": 0, "D6": 4, "D7": 2, "D8": 4, "D9": 0, "D10": 0}
    result = evaluate(model, policy)

    SOWs = sample_lhs(model, 1000)
    results = evaluate(model, update(SOWs, policy))
    print(results)

    results.as_dataframe(['performance', 'cost', 'risk', 'numOfUsers', 'latitude', 'sampEn', 'rainfall']).to_csv(
        r'../results/SD_results.csv')


# Scenario Discovery
def SD(results):
    print('\x1b[0;32;44m' + '************ Scenario Discovery using PRIM ************' + '\x1b[0m')
    print('\x1b[0;32;44m' + 'Policy : ' + '\x1b[0m')
    print(policy)
    classification = results.apply("'Effective' if performance > 5 else 'Ineffective'")
    p = Prim(results, classification, include=model.uncertainties.keys(), coi="Effective")
    box = p.find_box()
    # fig = box.show_tradeoff()

    # box.show_details()
    # plt.show()

    # Sensitivity Analysis
    print('\x1b[0;32;44m' + '************ Sensitivity Analysis ************' + '\x1b[0m')
    result_s = sa(model, "performance", policy=policy, method="sobol", nsamples=10000)
    print(result_s)
    fig = result_s.plot()


def main():
    # Initialize
    ts = Tradespace(0)
    numOfUsers = 100
    latitude = 45
    crop_type = 1

    # Calculate Pareto front from enumeration
    enum = ts.tradeSpace
    print('Number of Policies found: ' + str(len(enum)))
    nodes = ts.TS_nodes
    ts.plotTS()


if __name__ == "__main__":
    main()