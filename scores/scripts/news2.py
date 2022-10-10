# https://www.cebm.net/wp-content/uploads/2020/04/Trish-1.jpg
def main(heartRate, bloodPressure, temperature, bloodOxygen):
    total = 0
    # Respiratory rate: not used
    pass
    # Blood oxygen - scale1
    if bloodOxygen <= 91:
        total += 3
    elif 91 < bloodOxygen <= 93:
        total += 2
    elif 93 < bloodOxygen <= 96:
        total += 1
    # Blood oxygen - scale2: not relevant
    pass
    # Air or oxygen: none in this stage
    pass
    # Blood pressure
    if bloodPressure <= 90 or bloodPressure >= 220:
        total += 3
    elif 90 < bloodPressure <= 100:
        total += 2
    elif 100 < bloodPressure <= 110:
        total += 1
    # Heart rate
    if heartRate <= 40 or heartRate >= 131:
        total += 3
    elif 111 <= heartRate <= 130:
        total += 2
    elif 41 <= heartRate <= 50 or 91 <= heartRate <= 110:
        total += 1
    # Consciousness: none in this stage
    pass
    # Temperature
    if temperature <= 35.0:
        total += 3
    elif temperature >= 39.1:
        total += 2
    elif 35.1 <= temperature <= 36.0 or 38.1 <= temperature <= 39.0:
        total += 1
    
    return total
