from batch_20211116.batch_20211116_lib.util import position_time_series_append_benchmark_to_csv_png


# from builtins import False
result_position_path = 'D:/f_data/batch_20211116/step8_portfolio_time_series/' + 'position.csv'
path = 'D:/f_data/temp/amend/a.csv'
path2 = 'D:/f_data/temp/amend/b.png'




position_time_series_append_benchmark_to_csv_png(
    position_time_series_csv=result_position_path,
    input_time_col='date',
    input_position_col='roll',
    benchmark_ticker='amzn',
    output_time_series_csv=path,
    output_time_series_png=path2
)