def one_dot_round(inp: float):
    temp = inp - int(inp)
    if temp >= 0.5:
        return int(inp)+1
    else:
        return int(inp)


def coordinates_transform(coordinate: tuple):
    #  todo 等屏幕大小的配置文件写好之后，改成相应的
    return int(coordinate[0]), int(-coordinate[1]+600)