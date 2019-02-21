import pandas as pd


def link(data: list, mid='、', last='和')->str:
    '''把一个列表中的元素用mid和last链接起来,
    mid指的是列表中间元素之间的建个符号, 
    last指的是列表最后一个元素与之前元素的连接符号'''
    data = [str(d) for d in data]
    if len(data) == 1:
        return data[0]
    elif len(data) == 2:
        return last.join(data)
    else:
        t = mid.join(data[:-1])
        return last.join([t, data[-1]])


def eq_fields(ser1, ser2)->list:
    """获取ser1中等于ser2的index
    
    Arguments:
        ser1 {pd.Series} -- pandas.Series
        ser2 {Series or float or int} -- 比较标准
    
    Returns:
        list -- 返回满足条件的index的列表
    """
    cha = ser1 - ser2
    return list(cha[cha == 0].index)


def lt_fields(ser1, ser2)->list:
    """获取ser1中小于ser2的index
    
    Arguments:
        ser1 {pd.Series} -- pandas.Series
        ser2 {Series or float or int} -- 比较标准
    
    Returns:
        list -- 返回满足条件的index的列表
    """
    cha = ser1 - ser2
    return list(cha[cha < 0].index)


def gt_fields(ser1, ser2)->list:
    """获取ser1中大于ser2的index
    
    Arguments:
        ser1 {pd.Series} -- pandas.Series
        ser2 {Series or float or int} -- 比较标准
    
    Returns:
        list -- 返回满足条件的index的列表
    """
    cha = ser1 - ser2
    return list(cha[cha > 0].index)


def min_max(ser: pd.Series, splitor='~')->str:
    mi = ser.min()
    ma = ser.max()
    assert ma > mi
    return splitor.join(mi, ma)
