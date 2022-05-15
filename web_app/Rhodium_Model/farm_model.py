

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
            performance -= d_perf * (latitude / 1000)  # Account for the latitude effects
            performance += d_perf * (rainfall / 1000)
        if decision.description == 'ML Model':
            performance = performance - d_perf + (
                        -1 / 9 * (sampEn ** 2) + 1) * d_perf  # Account for the climate complexity effects
            risk = risk - d_risk + (-1 / 9 * (sampEn ** 2) + 1) * d_risk
        if decision.description == 'iOT Devices':
            hardware_cost += d_cost
        if decision.description == 'User Interface' or decision.description == 'Data Storage':
            maintenance_cost += d_cost
            if decision.description == 'Data Storage':
                data_storage_risk += d_risk

    maintenance_cost = hardware_cost + (maintenance_cost / numOfUsers)
    cost = maintenance_cost + hardware_cost * numOfUsers
    # predicted_yield = regression_rainfall_yield(crop_type, rainfall)
    risk += data_storage_risk
    policy_names = node['policy_names']

    return performance, cost, risk, node, policy_names

