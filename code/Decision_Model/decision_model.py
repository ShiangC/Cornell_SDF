
class Decision:
    def __init__(self, name, desc, importance, performance, cost, risk, priceVector):
        self.name = name
        self.description = desc
        self.yield_increase = performance['yield_increase']
        self.electricity = performance['electricity']
        self.water = performance['water']
        self.pesticides = performance['pesticides']
        self.labor = performance['labor']
        self.cs = performance['computation']
        self.importance = importance
        self.cost = cost
        self.risk = risk
        self.priceVector = priceVector

    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getPerf(self):
        yieldPerf = self.yield_increase * self.priceVector['yield']
        elecPerf = self.electricity * self.priceVector['electricity']
        waterPerf = self.water * self.priceVector['water']
        pesticidesPerf = self.pesticides * self.priceVector['pesticides']
        laborPerf = self.labor * self.priceVector['labor']
        return (yieldPerf * elecPerf + waterPerf + pesticidesPerf + laborPerf) * (1 + self.cs) * self.importance

    def getCost(self):
        return self.cost * self.importance

    def getRisk(self):
        return self.risk * self.importance


