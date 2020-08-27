
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

    def getName(self):
        return self.name

    def getDesc(self):
        return self.description

    def getPerf(self, priceVector):
        yieldPerf = self.yield_increase * priceVector['yield']
        elecPerf = self.electricity * priceVector['electricity']
        waterPerf = self.water * priceVector['water']
        pesticidesPerf = self.pesticides * priceVector['pesticides']
        laborPerf = self.labor * priceVector['labor']
        return (yieldPerf * elecPerf + waterPerf + pesticidesPerf + laborPerf) * (1 + self.cs)

    def getCost(self):
        return self.cost

    def getRisk(self):
        return self.risk


