from rhodium import *
import json
import math
from scipy.optimize import brentq as root
from j3 import J3
import numpy as np
import itertools

import os

os.environ['PATH'] += os.pathsep + r"/Users/zhaoyifan/Desktop/farmVal/J3"
os.system("J3.app input.csv")

decisions = []
# with open("decisions.json", "r") as read_file:
    
read = open("decisions.json", "r")
decisions = json.load(read)['Decisions']
read.close()
    

def farm_approach1(D1, D2, D3, D4, D5, D6, D7, D8, D9, D10,
                  numOfUsers = 100):
    #policy = [D1[0], D2, D3[0], D4, D5, D6[0], D7, D8[0], D9, D10]
    policy = [D1, D2, D3, D4, D5, D6, D7, D8, D9, D10]
    performance = 1
    
    for i in range(9):
        performance *= decisions[i]['decisions'][policy[i]]['performance'] #* decisions[i]['importance']
    
    IoT_cost = decisions[1]['decisions'][D2]['cost']

    UI_cost = decisions[2]['decisions'][D3]['cost'] 
    
    DataStorage_cost = decisions[4]['decisions'][D5]['cost']
    
    ML_risk = decisions[9]['decisions'][D10]['risk']
    DataStorage_risk = decisions[4]['decisions'][D5]['risk']
    
    cost = IoT_cost * numOfUsers + ((UI_cost + DataStorage_cost) / numOfUsers)
    risk = ML_risk + DataStorage_risk
    
    return (performance*100, cost, risk)

model = Model(farm_approach1)

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
                    Parameter("numOfUsers")]

model.responses = [Response("performance", Response.MAXIMIZE),
                   Response("cost", Response.MINIMIZE),
                   Response("risk", Response.MINIMIZE)]
model.constraints = []

DS_choices = [[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]
SF_choices = [0, 1, 2]

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

model.uncertainties = [NormalUncertainty("numOfUsers", 100, 20)]

output = optimize(model, "NSGAII", 100)
print("Found", len(output), "optimal policies!")
print(output)

J3(output.as_dataframe(['performance', 'cost', 'risk']))