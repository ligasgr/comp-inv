
# QSTK Imports
import QSTK.qstkutil.qsdateutil as du
import QSTK.qstkutil.tsutil as tsu
import QSTK.qstkutil.DataAccess as da

# Third Party Imports
import datetime as dt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import cPickle
import math



def main():
    dt_start = dt.datetime(2011, 1, 1)
    dt_end = dt.datetime(2011, 12, 31)
    symbols =['AAPL', 'GLD', 'GOOG', 'XOM']
    best_sharpe=0.0
    best_allocation = [0.0, 0.0, 0.0, 0.0]
    for first in range(0, 101, 10):
        for second in range(0, 101 - first, 10):
            for third in range(0, 101 - (first + second), 10):
                    for fourth in range(0, 101 - (first + second + third), 10):
                        if (first + second + third + fourth) == 100:
                            allocation = [first/100.0, second/100.0, third/100.0, fourth/100.0]
                            vol, avg, sharpe, cumulative_returns = simulate(dt_start, dt_end, symbols, allocation)
                            if sharpe > best_sharpe:
                                best_sharpe = sharpe
                                best_allocation = allocation
    print best_sharpe
    print best_allocation

def simulate(dt_start, dt_end, symbols, allocations):
    dt_timeofday = dt.timedelta(hours=16)
    ldt_timestamps = du.getNYSEdays(dt_start, dt_end, dt_timeofday)
    c_dataobj = da.DataAccess('Yahoo')
    ls_keys = ['open', 'high', 'low', 'close', 'volume', 'actual_close']
    ldf_data = c_dataobj.get_data(ldt_timestamps, symbols, ls_keys)
    d_data = dict(zip(ls_keys, ldf_data))
    df_rets = d_data['close'].copy()
    na_price = df_rets.values
    na_normalized_price = na_price / na_price[0, :]
    df_rets = df_rets.fillna(method='ffill')
    df_rets = df_rets.fillna(method='bfill')
    df_rets = df_rets.fillna(1.0)
    na_rets = na_normalized_price.copy() 
    tsu.returnize0(na_rets)
    na_portrets = np.sum(na_rets * allocations, axis=1)
    vol=np.std(na_portrets)
    avg_daily_returns=np.mean(na_portrets)
    sharpe= math.sqrt(252) * avg_daily_returns/vol
    cumulative_returns =  np.cumprod(na_portrets + 1, axis=0)

    return (vol, avg_daily_returns, sharpe, cumulative_returns[-1])

if __name__ == '__main__':
    main()
