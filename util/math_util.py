def one_dot_round(inp: float):
    temp = inp - int(inp)
    if temp >= 0.5:
        return int(inp)+1
    else:
        return int(inp)


def coordinates_transform(coordinate: tuple):
    #  todo 等屏幕大小的配置文件写好之后，改成相应的
    return int(coordinate[0]), int(-coordinate[1]+600)


def caculate_position_with_menu(rect: tuple, position: int, num_items: int):
    # todo 从相对位置计算 在screen上的绝对位置
    if abs(rect[2] - rect[0]) >= abs(rect[3] - rect[1]):  # 横向
        item_width = int(abs(rect[2] - rect[0]) / (num_items / 2 + 1))
        item_height = int(abs(rect[3] - rect[1]) / 2)
        item_start_x = rect[0] + (position - 1) * item_width
        if position % 2 == 0:
            item_start_y = rect[1] + item_height
        else:
            item_start_y = rect[1]
    else:  # 纵向
        item_width = int(abs(rect[2] - rect[0]) / 2)
        item_height = int(abs(rect[3] - rect[1]) / (num_items / 2 + 1))
        if position % 2 == 0:
            item_start_x = rect[0] + item_width
        else:
            item_start_x = rect[0]
        item_start_y = rect[1] + (position - 1) * item_height
    item_end_x = item_start_x + item_width
    item_end_y = item_start_y + item_height
    return (item_start_x, item_start_y), (item_end_x, item_end_y)


