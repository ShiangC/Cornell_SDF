
class Decision:
    def __init__(self, performance, cost, risk):
        self.yield_increase = performance['yield_increase']
        self.electricity = performance['electricity']
        self.water = performance['water']
        self.pesticides = performance['pesticides']
        self.labor = performance['labor']
        self.cost = cost
        self.risk = risk

    # Calculate the performance of the decision

