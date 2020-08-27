# Maps crop type to a linear regression between rainfall and crop yield
def regression_rainfall_yield(crop_type, rainfall):
    if crop_type is 1:  # Linear regression for Wheat
        return 0.0000037434 * rainfall - 0.01301198
    if crop_type is 2:  # Linear regression for Potato
        return -0.00029371 * rainfall + 0.81806965
    if crop_type is 3:  # Linear regression for Grape
        return 0.07286135 * rainfall - 18.21006311