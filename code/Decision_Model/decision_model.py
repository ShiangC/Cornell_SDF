
class Decision:
    def __init__(self, name, desc, performance, cost, risk):
        self.name = name
        self.description = desc
        self.yield_increase = performance['yield_increase']
        self.electricity = performance['electricity']
        self.water = performance['water']
        self.pesticides = performance['pesticides']
        self.labor = performance['labor']
        self.cs = performance['computation']
        self.cost = cost
        self.risk = risk

    # Calculate the performance of the decision

