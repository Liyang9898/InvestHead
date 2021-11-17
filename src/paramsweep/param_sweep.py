from numpy.random.bounded_integers import np

from loaddata.loadst2df import load_st_data
import pandas as pd
from paramsweep.util import gen_date_rage_list
from runner.run_strat import run_strat


threshold = 0.25
stop_gain_list = np.arange(1,5,0.5)
stop_loss_list = np.arange(1,5,0.5)
ds_range_list = gen_date_rage_list('2008-01-01','2020-01-01', 90)

opentop = True
# opentop = False

# timescope = '1min'
# timescope = '5min'
timescope = '1min_12years'
# timescope = '5min_12years'

plot = False
# plot = True
dynamic_stop=False
# dynamic_stop=True

df= load_st_data(timescope)


print(df)
print('start_sweep')
param_res = []
for ds_range in ds_range_list:
    for stop_gain in stop_gain_list:
        for stop_loss in stop_loss_list:
            for opentop in [True, False]:
                print('sweeping: ' + ds_range['s'] + ', ' + ds_range['e'])
                stat = run_strat(
                    stop_gain=stop_gain,
                    stop_loss=stop_loss,
                    threshold=threshold,
                    opentop=opentop,
                    df=df,
                    start_time=ds_range['s'],
                    end_time=ds_range['e'],
                    plot = plot,
                    dynamic_stop=dynamic_stop
                )
                param_res.append(stat)
                print(stat)

df = pd.DataFrame(param_res)
path_out_1 = """D:/f_data/param_sweep_1m.csv"""
path_out_2 = """D:/f_data/param_sweep_5m.csv"""
path_out_3 = """D:/f_data/param_sweep_5m_2008_2020.csv"""
path_out_4 = """D:/f_data/param_sweep_1m_2008_2020.csv"""
df.to_csv(path_out_4,index=False)
print('done')