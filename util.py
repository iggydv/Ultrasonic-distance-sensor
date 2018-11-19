def calcAverage(prev, cur):
    return 0.7 * prev + 0.3 * cur

def calcVelocity(prev, cur, deltaT):
    if deltaT > 0:
        return (cur - prev) / deltaT * 0.036
    else:
        return 0

