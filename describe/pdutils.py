import pandas as pd


def loc(df, s1, s2=None):
    if isinstance(df, pd.Series):
        return df.loc[s1]
    if s2 is None:
        return df.loc[s1]
    return df.loc[s1, s2]
