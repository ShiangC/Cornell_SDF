import json
from .decision_model import Decision
from itertools import combinations, product
import numpy as np
import matplotlib.pyplot as plt
import oapackage
import pandas as pd
from j3 import J3


class Tradespace:

    def __init__(self, crop_type, priceVector):
        self.policy = []
        self.decision_num = 10
        self.crop_type = crop_type
        self.priceVector = priceVector
        self.decision_pool = self.make_decision_pool()
        self.tradeSpace = self.enumerateTS()
        self.TS_nodes = list(map(self.makeNodes, self.tradeSpace))

    # Produce a pool of decisions
    def make_decision_pool(self):
        json_decisions = []
        read = open("Decision_Model/decision_dylan.json", "r")
        json_decisions = json.load(read)['Decisions']
        read.close()
        decsion_pool = []
        for decision in json_decisions:
            archs = {
                'desc': decision['description'],
                'type': decision['type'],
                'alternatives': [Decision(d['alternative'], decision['description'], decision['importance'],
                                          d['performance'], d['cost'], d['risk'], self.priceVector) for d in decision['decisions']]
            }
            decsion_pool.append(archs)
            print(archs)
        return decsion_pool

    # Create a list representing a policy
    def make_policy(self, d_list):
        policy = []
        for i in range(self.decision_num):
            policy.append(self.decision_pool[i][d_list[i]])
        self.policy = policy
        return policy

    # Enumerate all decisions to generate a trade-space of all possible policies
    def enumerateTS(self):
        policy_pool = []
        for archs in self.decision_pool:
            decisions = archs['alternatives']
            decisions_type = archs['type']
            print('Architectures:  ' + str(list(map(Decision.getName, decisions))))
            combs = []

            # Calculate combinations of a Down-selecting type of decision
            if decisions_type == 'DS':
                for i in range(len(decisions)):
                    for comb in list(combinations(decisions, i+1)):
                        combs.append(comb)
            # Standard-form type decision has no combination
            else:
                for d in decisions:
                    combs.append((d,))

            if not policy_pool:
                policy_pool = combs
            else:
                policy_pool = self.__flattenList(list(product(policy_pool, combs)))

        return policy_pool

    def makeNodes(self, policy):
        perfVector = {
                'yield': 0,
                'electricity': 0,
                'water': 0,
                'pesticides': 0,
                'labor': 0
            }
        total_perf = 0
        total_cost = 0
        total_risk = 0

        for decision in policy:
            perfVector = decision.getPerf(perfVector)
            total_cost += decision.getCost()
            total_risk += decision.getRisk()

        for key, value in perfVector.items():
            total_perf += value

        # return {
        #     'policy_names': list(map(Decision.getName, policy)),
        #     'perf': 1- np.exp(-total_perf),
        #     'cost': total_cost,
        #     'risk': 1-np.exp(-total_risk),
        #     'perfVector': perfVector,
        #     'policy_num': len(policy),
        #     'policy': policy
        #     }
        return {
            'policy_names': list(map(Decision.getName, policy)),
            'perf': total_perf,
            'cost': total_cost,
            'risk': total_risk,
            'perfVector': perfVector,
            'policy_num': len(policy),
            'policy': policy
            }

    def calcPareto(self):
        # find optimal designs
        pareto = oapackage.ParetoDoubleLong()
        i = 0
        for node in self.TS_nodes:
            w = oapackage.doubleVector((node['perf'], -1 * node['cost'], -1 * node['risk']))
            pareto.addvalue(w, i)
            i += 1
        pareto.show(verbose=1)

        lst = pareto.allindices()  # the indices of the Pareto optimal designs
        optimal_set = []
        for i in lst:
            optimal_set.append(self.TS_nodes[i])

        return optimal_set


    def plotTS(self, optimal_set):
        ax = plt.axes(projection='3d')
        # find optimal designs
        # pareto = oapackage.ParetoDoubleLong()
        # i = 0
        # for node in self.TS_nodes:
        #     w = oapackage.doubleVector((node['perf'], -1 * node['cost'], -1 * node['risk']))
        #     pareto.addvalue(w, i)
        #     i += 1
        # pareto.show(verbose=1)
        #
        # lst = pareto.allindices()  # the indices of the Pareto optimal designs
        # df = pd.DataFrame(self.TS_nodes)
        # optimal_set = []
        # for i in lst:
        #     optimal_set.append(self.TS_nodes[i])
        # optimal_set = pd.DataFrame(optimal_set)

        optimal_set = pd.DataFrame(optimal_set)
        pd.DataFrame(self.TS_nodes).to_csv(r'../web_app/static/tradespace_enumeration.csv')
        optimal_set.to_csv(r'../web_app/static/pareto_set.csv')
        # 3d plots
        df = pd.DataFrame(self.TS_nodes)
        h = plt.plot(df['perf'], df['cost'], df['risk'], '.b', markersize=8, label='Non Pareto-optimal')
        hp = plt.plot(optimal_set['perf'], optimal_set['cost'], optimal_set['risk'], '.y', markersize=4, label='Pareto optimal')
        ax.set_xlabel('Performance')
        ax.set_ylabel('Cost')
        ax.set_zlabel('Risk')
        _ = plt.title('Pareto Front', fontsize=15)
        plt.savefig('../web_app/static/pareto_ts.png')

    # Calculating the total benefit from yield increase
    def calc_r1(self, crop_price):
        r1 = 0
        for d in self.policy:
            r1 += d.yield_increase
        return r1*crop_price

    # Calculating the total benefit from saved electricity
    def calc_e1(self, e_price):
        e1 = 0
        for d in self.policy:
            e1 += d.electricity
        return e1 * e_price

    # Calculating the total benefit from saved water usage
    def calc_e2(self, w_price):
        e2 = 0
        for d in self.policy:
            e2 += d.water
        return e2 * w_price

    # Calculating the total benefit from saved pesticides
    def calc_e3(self, p_price):
        e3 = 0
        for d in self.policy:
            e3 += d.pes
        return e3 * p_price

    # Calculating the total computational stability
    def calc_e4(self):
        e4 = 0
        for d in self.policy:
            e4 += d.cs
        return e4

    # place holder: function calculating total cost of a policy
    def calc_cost(self):
        total_cost = 0
        for d in self.policy:
            total_cost += d.cost
        return total_cost

    # place holder: function calculating total risk of a policy
    def calc_risk(self):
        total_risk = 0
        for d in  self.policy:
            total_risk += d.risk
        return total_risk

    # mapper function to help format lists
    def __flattenList(self, policy_pool):
        res = []
        for policy in policy_pool:
            ls = []
            for comb in policy:
                for decision in comb:
                    if type(decision) is tuple:
                        for obj in decision:
                            ls.append(obj)
                    else:
                        ls.append(decision)
            res.append(ls)
        return res


def crossMap():
    test_list1 = [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    test_list2 = [('x',), ('y',), ('z',), ('x', 'y'), ('x', 'z'), ('y', 'z'), ('x', 'y', 'z')]
    test_list3 = [1, 2, 3]
    test_list4 = ['x', 'y']
    # printing original lists
    print("The original list 1 is : " + str(test_list1))
    print("The original list 2 is : " + str(test_list2))

    # Extract Combination Mapping in two lists
    # using zip() + product()
    # print(list(product(test_list2, repeat=len(test_list1))))
    comb1 = list(combinations(test_list3, 2))
    comb2 = list(combinations(test_list4, 2))
    # res = []
    # for comb in comb2:
    #     print(comb)
    #     for ele in product(comb, repeat=len(comb1)):
    #         print(ele)
    #         temp = list(zip(comb1, ele))
    #         res.append(temp)
    res = list(product(test_list1, test_list2))
    # printing result
    print("Mapped Combination result : " + str(res))


# def main():
#     ts = Tradespace(0)
#     # ts.make_policy([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
#     # for decision in ts.policy:
#     #     ts.print_decision(decision)
#     # print('Yield Increase:     ' + str(ts.calc_r1(100)))
#     # print('Electricity Saved:  ' + str(ts.calc_e1(1)))
#     # print('Water Saved:        ' + str(ts.calc_e2(10)))
#     # print('Computational Stability: ' + str(ts.calc_e4()))
#
#     # small_pool = list(ts.decision_pool[i] for i in range(10))
#     # print(small_pool)
#     # enum = enumerateTS(small_pool)
#     # for policy in enum:
#     #     print(list(map(Decision.getName, policy)))
#     enum = ts.tradeSpace
#     print('Number of Policies found: ' + str(len(enum)))
#     nodes = ts.TS_nodes
#     ts.plotTS()

# if __name__ == "__main__":
#     main()

