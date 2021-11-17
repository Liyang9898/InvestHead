from loaddata.loadst2df import load_st_data
from runner.run_strat_multi_trade import run_strat_bug_bar

start_time = '2007-01-30'
end_time = '2020-01-08'
threshold = 0.25
stop_loss = 2
stop_gain = 1

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

stat = run_strat_bug_bar(
    stop_gain=stop_gain,
    stop_loss=stop_loss,
    threshold=threshold,
    opentop=opentop,
    df=df,
    start_time=start_time,
    end_time=end_time,
    plot = plot,
    dynamic_stop=dynamic_stop,
    bigbarsize=2
)
print(stat)