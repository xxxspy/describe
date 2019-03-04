import re
from decimal import Decimal
from pandas import Series
import pandas as pd
import numpy as np
from typing import *


def trueround(number: float, places: int = 0):
    '''
    trueround(number, places)

    example:

        >>> trueround(2.55, 1) == 2.6
        True

    uses standard functions with no import to give "normal" behavior to 
    rounding so that trueround(2.5) == 3, trueround(3.5) == 4, 
    trueround(4.5) == 5, etc. Use with caution, however. This still has 
    the same problem with floating point math. The return object will 
    be type int if places=0 or a float if places=>1.

    number is the floating point number needed rounding

    places is the number of decimal places to round to with '0' as the
        default which will actually return our interger. Otherwise, a
        floating point will be returned to the given decimal place.

    Note:   Use trueround_precision() if true precision with
            floats is needed

    GPL 2.0
    copywrite by Narnie Harshoe <signupnarnie@gmail.com>
    '''
    place = 10 ** (places)
    rounded = (int(number * place + 0.5 if number >= 0 else -0.5)) / place
    if rounded == int(rounded):
        rounded = int(rounded)
    return rounded


def trueround_precision(number, places=0, rounding=None) -> Decimal:
    '''
    trueround_precision(number, places, rounding=ROUND_HALF_UP)

    Uses true precision for floating numbers using the 'decimal' module in
    python and assumes the module has already been imported before calling
    this function. The return object is of type Decimal.

    All rounding options are available from the decimal module including 
    ROUND_CEILING, ROUND_DOWN, ROUND_FLOOR, ROUND_HALF_DOWN, ROUND_HALF_EVEN, 
    ROUND_HALF_UP, ROUND_UP, and ROUND_05UP.

    examples:

        >>> trueround(2.5, 0) == Decimal('3')
        True
        >>> trueround(2.5, 0, ROUND_DOWN) == Decimal('2')
        True

    number is a floating point number or a string type containing a number on 
        on which to be acted.

    places is the number of decimal places to round to with '0' as the default.

    Note:   if type float is passed as the first argument to the function, it
            will first be converted to a str type for correct rounding.

    GPL 2.0
    copywrite by Narnie Harshoe <signupnarnie@gmail.com>
    '''
    from decimal import ROUND_HALF_UP
    from decimal import ROUND_CEILING
    from decimal import ROUND_DOWN
    from decimal import ROUND_FLOOR
    from decimal import ROUND_HALF_DOWN
    from decimal import ROUND_HALF_EVEN
    from decimal import ROUND_UP
    from decimal import ROUND_05UP

    if pd.isnull(number):
        return number
    if type(number) == type(float()):
        number = str(number)
    if rounding == None:
        rounding = ROUND_HALF_UP
    place = '1.'
    for i in range(places):
        place = ''.join([place, '0'])
    return Decimal(number).quantize(Decimal(place), rounding=rounding)


def trueround_series(ser: Series, places=0, rounding=None) -> Series:
    def f(x):
        if isinstance(x, str):
            x = x.strip()
            if x:
                try:
                    x = float(x)
                except:
                    return x
                return trueround_precision(
                    x, places=places, rounding=rounding)
            else:
                return None
        x = float(x)
        return trueround_precision(
            x, places=places, rounding=rounding)

    return ser.map(f, na_action='ignore')


def format_percent(data: Series or float, places=1, rounding=None, max100=True, int0=True, par=100):
    '''
    data: 需要格式化的数据
    places: 小数位数
    rounding: 保留小数位数的方法
    max100: 限制百分比的最大值为100%
    int0: 强制将0.0%和100.0%转换为0%和100%
    '''

    data = data * par
    if isinstance(data, Series):
        rtn = trueround_series(data, places=places, rounding=rounding)
    else:
        rtn = trueround_precision(data, places=places, rounding=rounding)
    if max100:
        rtn = max_100(rtn)
    if int0:
        rtn = filter_0_100(rtn)
    return rtn


def filter_0_100(value: float or Decimal or Series):
    '''过滤100.0和0.0
    return 100或0'''
    if isinstance(value, Series):
        def fil(x):
            if x in (0, 100):
                return trueround_precision(x, 0)
            if x > 100:
                x = 100
                return trueround_precision(x, 0)
            return x

        return value.map(fil)
    if value in (0, 100):
        return trueround_precision(value, 0)
    return value


def max_100(value: float or Decimal or Series):
    '''最大值不能超过100, 否则返回Decimal(100)'''
    if isinstance(value, Series):
        return value.map(lambda x: Decimal('100') if x > 100 else x)
    if value > 100:
        return Decimal('100')
    return value


def get_percent(ser: Series, index):
    '''获取百分比的时候防止出现`KeyError`'''
    try:
        return ser.loc[index]
    except KeyError:
        return Decimal('0')


def df_one_index(df: pd.DataFrame)->pd.DataFrame:
    index = df.index
    while isinstance(index, pd.MultiIndex):
        index = index.droplevel(0)
    df.index = index
    return df


def df_decimal(df: pd.DataFrame, places=None)->pd.DataFrame:
    if isinstance(places, dict):
        for vname, place in places.items():
            df[vname] = trueround_series(df[vname], place)
    elif isinstance(places, (list, tuple)):
        for i, place in enumerate(places):
            c = df.columns[i]
            df[c] = trueround_series(df[c], place)
    elif isinstance(places, int):
        for c in df.columns:
            df[c] = trueround_series(df[c], places)
    return df


def str2float(num: str, places=None)->Decimal:
    num = float(num)
    if places is not None:
        num = trueround_precision(num, places=places)
    return num


def mean_sd(mean, sd, mean_place=3, sd_place=3, format='{mean}({sd})'):
    return format.format(
        mean=decimal(mean, mean_place),
        sd=decimal(sd, sd_place)
    )


def mean_sd_series(means: pd.Series, sds: pd.Series,
                   mean_place=3, sd_place=3)->pd.Series:
    '''把平均值和标准差列合并成一列'''
    means = trueround_series(means, mean_place)
    sds = trueround_series(sds, sd_place)
    data = []
    for i in range(means.shape[0]):
        m = means.iloc[i]
        sd = sds.iloc[i]
        data.append('{}({})'.format(
            m, sd
        ))
    return pd.Series(data, index=means.index)


dunhao = '、'
douhao = '，'

lATENT_STARTER = 'L_'
ERROR_STARTER = 'e_'


def latent_varname(name: str)->str:
    if not name.startswith(lATENT_STARTER):
        name = lATENT_STARTER + name
    return name


def strip_latent(name: str)->str:
    return name.strip(lATENT_STARTER)


def error_varname(name: str)->str:
    if not name.startswith(ERROR_STARTER):
        name = ERROR_STARTER + name
    return name


def clean_value(value):
    '''有一些值会带有标注, 比如(a), 需要删除'''
    if isinstance(value, str):
        for i in 'abcdef':
            value = value.strip('(' + i + ')')
        value = value.strip('*')
    return value


def sig(value):
    value = clean_value(value)
    if float(value) < 0.001:
        return 'P<.001'
    if float(value) < 0.01:
        return 'p<.01'
    if float(value) < 0.05:
        return 'p<.05'
    else:
        return 'p>.05'


def star(p):
    if float(p) < .001:
        return '***'
    if float(p) < .01:
        return '**'
    if float(p) < .05:
        return '*'
    return ''


def f_des(df1, df2, f, p):
    return 'F({},{}) = {}, {}'.format(int(df1), int(df2), f, sig(p))

def t_des(t, df, p):
    p = sig(p)
    return 't={},df={},{}'.format(t, df, p)

def chi_des(chi, df, p):
    p = sig(p)
    return 'chi2={},df={},{}'.format(chi, df, p)


def value_star(v, p, place=1):
    '''
    v: 4.5
    p: < .01
    return 4.5**
    '''
    v = decimal(v, place)
    return '{}{}'.format(v, star(p))


def decimal(value, place):
    '''保留小数位数,
    如果value是字符串, 就会被转换成float'''
    fmt = '{{0:.{}f}}'.format(place)
    return fmt.format(float(value))


def compress_index(index: pd.MultiIndex)->pd.Index:
    '''把多层index压缩成1层'''
    if not isinstance(index, pd.MultiIndex):
        return index
    new_index = []
    for ii in index:
        new_ii = ''
        for i in ii:
            if not pd.isnull(i):
                new_ii += str(i)
        new_index.append(new_ii)
    return pd.Index(new_index)