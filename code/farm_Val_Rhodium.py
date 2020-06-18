from rhodium import *
import json
import math
from scipy.optimize import brentq as root
from j3 import J3
import numpy as np
import itertools
import csv

# plotting options
# %matplotlib inline
# sns.set()
# sns.set_style('darkgrid')
print('\x1b[6;30;42m' + '************ Welcome to FarmVal Tradespace Exploration Tool ************' + '\x1b[0m')
input_numOfUsers = int(input("Please enter an estimation for the mean number of users:"))
input_latitude = int(input("Please enter an estimation for the mean latitude:"))

json_decisions = []
# with open("decisions.json", "r") as read_file:
    
read = open("decisions.json", "r")
json_decisions = json.load(read)['Decisions']
read.close()
    
#print(decisions[0])


def farm_approach2(D1, D2, D3, D4, D5, D6, D7, D8, D9, D10,
                   decisions = json_decisions,
                   numOfUsers = input_numOfUsers,
                   latitude = input_latitude,
                   sampEn = 2.68):

    policy = [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10]
    performance = 1
    
    #Account for latitude changes
    decisions[5]['decisions'][policy[5]]['performance'] *= (1 - (latitude/1000))
    decisions[2]['decisions'][policy[2]]['performance'] *= (1 - (latitude/1000))

    #Regional Climate complexity (sampEn) affects ML performance and risk
    # decisions[9]['decisions'][policy[9]]['performance'] *= (-1/9 * (sampEn ** 2) + 1)
    #decisions[9]['decisions'][policy[9]]['risk'] += (-1/9 * (sampEn ** 2) + 1)
    
    for i in range(9): 
        performance *= decisions[i]['decisions'][policy[i]]['performance']
        if i is 2 or i is 5:
            performance *= (1 - (latitude/1000))
        elif i is 9:
            performance *= (-1/9 * (sampEn ** 2) + 1)
    
    IoT_cost = decisions[1]['decisions'][D2]['cost']
    UI_cost = decisions[2]['decisions'][D3]['cost'] 
    DataStorage_cost = decisions[4]['decisions'][D5]['cost']
    
    ML_risk = decisions[9]['decisions'][D10]['risk']
    DataStorage_risk = decisions[4]['decisions'][D5]['risk']
    
    matainance_cost = IoT_cost + (UI_cost + DataStorage_cost)/numOfUsers
    hardware_cost = IoT_cost * numOfUsers
    
    cost = matainance_cost + hardware_cost
    risk = (ML_risk * (-1/9 * (sampEn ** 2) + 1)) + DataStorage_risk
    
    return (performance, cost, risk)

#Setting up Rhodium Model
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
                    Parameter("sampEn")]

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

#Optimization
output = optimize(model, "NSGAII", 100)
print('\x1b[0;32;44m' + "Found", len(output), "optimal policies!" + '\x1b[0m')
print(output)
output.as_dataframe(['performance', 'cost', 'risk']).to_csv(r'../results/pareto_policies.csv')


#Policy Evaluation
model.uncertainties = [NormalUncertainty("numOfUsers", input_numOfUsers, 100),
                       NormalUncertainty("latitude", input_latitude, 3),
                       NormalUncertainty("sampEn", 2.68, 0.136)]
policy = {"D1" : 4,"D2":0, "D3":3, "D4":1, "D5":0, "D6":4, "D7":2, "D8":4, "D9":0, "D10":0}
result = evaluate(model, policy)

SOWs = sample_lhs(model, 1000)
results = evaluate(model, update(SOWs, policy))
print(results)

results.as_dataframe(['performance', 'cost', 'risk', 'numOfUsers', 'latitude', 'sampEn']).to_csv(r'../results/SD_results.csv')

#Scenario Discovery
print('\x1b[0;32;44m' + '************ Scenario Discovery using PRIM ************' + '\x1b[0m')
print('\x1b[0;32;44m' + 'Policy : ' + '\x1b[0m')
print(policy)
classification = results.apply("'Effective' if performance > 1.5 else 'Ineffective'")
p = Prim(results, classification, include=model.uncertainties.keys(), coi="Effective")
box = p.find_box()
# fig = box.show_tradeoff()

# box.show_details()
# plt.show()

#Sensitivity Analysis
print('\x1b[0;32;44m' + '************ Sensitivity Analysis ************' + '\x1b[0m')
result_s = sa(model, "performance", policy=policy, method="sobol", nsamples=10000)
print(result_s)
fig = result_s.plot()