
LABEL_ADJUST = 'label_adjust'


# absolute profitable range: [S,S2] inclusive - price in range must be 1 % higher than lowest
S = 's' # first date of the adjustment drop
S2 = 's2' # last date for placing short order and get profit after entry date (how to define profit?->1.5% and not same day in and out)
E = 'e' # last date of adjustment drop



adjustments = [
#     {'s':'2021-05-10',S2:'2021-05-11','e':'2021-05-12'},
    {'s':'2021-03-18',S2:'2021-03-23','e':'2021-03-25'},
    {'s':'2021-02-19',S2:'2021-03-03','e':'2021-03-04'},
    {'s':'2021-01-27',S2:'2021-01-28','e':'2021-01-29'},
    {'s':'2020-10-14',S2:'2020-10-27','e':'2020-10-30'},
    {'s':'2020-09-03',S2:'2020-09-22','e':'2020-09-24'},
#     {'s':'2020-10-14',S2:'','e':'2020-11-02'},
#     {'s':'2020-06-10',S2:'','e':'2020-07-01'},
#     {'s':'2020-02-21',S2:'','e':'2020-03-25'},
#     {'s':'2020-01-24',S2:'','e':'2020-02-04'},
#     {'s':'2019-09-20',S2:'','e':'2019-10-10'},
#     {'s':'2019-07-31',S2:'','e':'2019-08-29'},
#     {'s':'2019-05-06',S2:'','e':'2019-06-04'}
]