import json
from Decision_Model.decision_model import Decision


class Tradespace:

    def __init__(self, crop_type):
        self.decision_pool = self.make_decision_pool()
        self.policy = []
        self.decision_num = 10
        self.crop_type = crop_type

    # Produce a pool of decisions
    def make_decision_pool(self):
        json_decisions = []
        read = open("Decision_Model/decision_evaluation.json", "r")
        json_decisions = json.load(read)['Decisions']
        read.close()
        decsion_pool = []
        for decision in json_decisions:
            archs = [Decision(d['alternative'], decision['description'], d['performance'], d['cost'], d['risk']) for d in decision['decisions']]
            decsion_pool.append(archs)
        return decsion_pool

    # Create a list representing a policy
    def make_policy(self, d_list):
        policy = []
        for i in range(self.decision_num):
            policy.append(self.decision_pool[i][d_list[i]])
        self.policy = policy
        return policy

    def print_decision(self, decision):
        print('--------- ' + decision.description + ': ' + decision.name)

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


def enumerate_policy(ts):
    enum = []
    for d1 in range(3):
        for d2 in  range(3):
            for d3 in range(3):
                policy = ts.make_policy([d1, d2, d3, 1, 1, 1, 1, 1, 1, 1])
                res = {
                    "policy": policy,
                    "r1": ts.calc_r1(100),
                    "e1": ts.calc_e1(1),
                    "e2": ts.calc_e2(10),
                    "e4": ts.calc_e4()
                }
                enum.append(res)
    return enum


def main():
    ts = Tradespace(0)
    # ts.make_policy([1, 1, 1, 1, 1, 1, 1, 1, 1, 1])
    # for decision in ts.policy:
    #     ts.print_decision(decision)
    # print('Yield Increase:     ' + str(ts.calc_r1(100)))
    # print('Electricity Saved:  ' + str(ts.calc_e1(1)))
    # print('Water Saved:        ' + str(ts.calc_e2(10)))
    # print('Computational Stability: ' + str(ts.calc_e4()))
    enum = enumerate_policy(ts)
    print(len(enum))


if __name__ == "__main__":
    main()
