import streamlit as st
import numpy as np
import pandas as pd
import time
from enum import Enum
from strategy import Strategy
from strategy import States
import datetime
import matplotlib.pyplot as plt
import os
import sys
import string

stgy = Strategy()
date_coloumn_name = '日期'
close_coloumn_name = '收盘'
open_coloumn_name = '开盘'
# year_coloumn_name = 
open_rate = 'open_rate'
close_rate = 'close_rate'

# 读取当前文件夹下的数据列表
# sys.path.append("/home/ronovo/PycharmProjects/pythonProject")
all_csv_files = []
all_dates = []
cur_path = os.path.dirname(os.path.abspath(__file__)) 
st.write(cur_path)

for f in os.listdir(cur_path):
    if '.csv' == os.path.splitext(f)[1]:
        all_csv_files.append(f)
        all_dates.append(datetime.date(int(f.split("_")[1]),int(f.split("_")[2]),int(f.split("_")[3])))

choose_date = st.date_input('选择需要绘制的日期',datetime.date(2023,5,17))
sorted_all_dates = sorted(all_dates,key=lambda x:datetime.datetime(x.year,x.month,x.day).timestamp())
file_name_choose = 'A50_' + choose_date.strftime('%Y_%m_%d') + '_klt1.csv'


if os.path.exists(file_name_choose):
    df_old = pd.read_csv(file_name_choose)
    print('df_old = ',df_old)
    df_choose_year = df_old[pd.DatetimeIndex(df_old[date_coloumn_name]).year  == choose_date.year ]
    df_choose_month = df_choose_year[pd.DatetimeIndex(df_choose_year[date_coloumn_name]).month  == choose_date.month]
    df_choose_day = df_choose_month[pd.DatetimeIndex(df_choose_month[date_coloumn_name]).day  == choose_date.day]
    base = df_choose_day[open_coloumn_name].iloc[0]
    df_choose_day[open_rate] = df_choose_day.apply(lambda x : x[open_coloumn_name]/base*100 - 100,axis=1)
    df_choose_day[close_rate] = df_choose_day.apply(lambda x : x[close_coloumn_name]/base*100 - 100,axis=1)


    fig = plt.figure(str(choose_date))
    plt.plot(df_choose_day[date_coloumn_name],df_choose_day[close_rate])

    plt.scatter(df_choose_day[date_coloumn_name].iloc[0],df_choose_day[close_rate].iloc[0],marker='o',color='green')

    for i in range(0,df_choose_day.shape[0]):
        stgy.state_machine_run(df_choose_day.iloc[i])
        if stgy.current_state == States.Sell:
            plt.scatter(df_choose_day[date_coloumn_name].iloc[i],df_choose_day[close_rate].iloc[i],marker='o',color='red')

    st.pyplot(fig)

else:
    st.write('该日期无对应数据文件')
