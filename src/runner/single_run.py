from loaddata.loadst2df import load_st_data
from runner.run_strat import run_strat

start_time = '2010-01-01'
end_time = '2020-01-01'
threshold = 0.25
stop_loss = 16
stop_gain = 1
daytrade_endtime='16:30:00'

# opentop = True
opentop = False

# timescope = '1min'
# timescope = '5min'
# timescope = '1min_12years'
timescope = '5min_12years'

# plot = False
plot = True
dynamic_stop=False
# dynamic_stop=True

df= load_st_data(timescope)

print(df)


stat = run_strat(
    stop_gain=stop_gain,
    stop_loss=stop_loss,
    threshold=threshold,
    opentop=opentop,
    df=df,
    start_time=start_time,
    end_time=end_time,
    daytrade_endtime=daytrade_endtime,
    plot = plot,
)
for k,v in stat.items():
    print(k,v)