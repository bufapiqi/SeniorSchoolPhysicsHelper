def one_dot_round(inp: float):
    temp = inp - int(inp)
    if temp >= 0.5:
        return int(inp)+1
    else:
        return int(inp)

def coordinates_transform(coordinate: tuple):
    pass