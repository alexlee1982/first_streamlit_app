import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time
import matplotlib as mpl
from scipy import stats
from enum import Enum


date_coloumn_name = '日期'
close_coloumn_name = 'close_rate'
open_coloumn_name = 'open_rate'


class States(Enum):
    Init = 1
    Buy = 2
    Wait = 3
    Wait_sell = 4
    Time_Expire = 5
    Sell = 6
    End = 7


class Strategy(object):
    def __init__(self) -> None:
        pass

    current = 0.0
    cost = 0.0
    max = 0.0
    median = 0.59
    mean = 1.464000941715851
    current_state = States.Init
    

    def state_machine_run(self,data):
        self.current = data[close_coloumn_name]
        current_hour = pd.to_datetime(data[date_coloumn_name],format='%Y-%m-%d %H:%M').hour
        current_minute = pd.to_datetime(data[date_coloumn_name],format='%Y-%m-%d %H:%M').minute
        # print(' current_hour = ',current_hour,'current_minute = ',current_minute)
        if States.Init == self.current_state:
            # 读取当前数据时间
            if current_hour == 9 and  current_minute >= 30:
                #调用记录买取，按照open，实际可能需要其它操作来实现这个功能
                self.cost = data[open_coloumn_name]
                print("entry Wait cost = ",self.cost)
                # 进入到下一步
                self.current_state = States.Wait

        if States.Wait == self.current_state:
            # 时间耗尽
            if current_hour >= 14 and  current_minute >= 55:
                self.current_state = States.Time_Expire
                                
            # 等待当前值超过cost
            if self.current > self.cost + self.median + 2.5/10000:
                print(" entry Wait_sell current = ",self.current," cost = ",self.cost)
                self.current_state = States.Wait_sell
                self.max = self.current

        if States.Wait_sell == self.current_state:
            if self.current > self.max:
                self.max = self.current
            # 时间耗尽
            if current_hour >= 14 and  current_minute >= 55:
                self.current_state = States.Time_Expire
            
            if self.current < self.max *0.7 and self.current > 0:
                print(" entry Sell current = ",self.current," cost = ",self.cost," max = ",self.max)
                self.current_state = States.Sell
                return

        if States.Time_Expire == self.current_state:
            self.current_state = States.Sell
            return
            
        if States.Sell == self.current_state:
            # 调用sell功能
            self.current_state = States.End
        
        if States.End == self.current_state:
            pass

        # print(' current_state = ',self.current_state)


        
