# -- coding: utf-8 --
"""preparingDataset.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vKx7w3_2FZ1Lyldvd7Xwee4ranOGCLBo
"""

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import datetime

class RiskPredictor:
  def __init__(self):
    self.low = [["Drive Brake Control",1,2],["Fuel Level",1,1],["Misc Air Filter Pressure",20,2]]
    self.low_df = pd.DataFrame(self.low,columns = ["Parameter","Threshold","Probability"])

    self.lowhigh = [["Engine Oil Pressure",25,65,3],["Drive Transmission Pressure",200,450,2],["Fuel Pressure",35,65,1],["Misc System Voltage",12.0,15.0,3]]
    self.lowhigh_df = pd.DataFrame(self.lowhigh,columns = ["Parameter","Threshold Low","Threshold High","Probability"])

    self.high = [["Engine Speed",1800,2],["Engine Temperature",105,3],["Drive Pedal Sensor",4.7,1],["Fuel Water Fuel",1800,3],["Fuel Temparature",400,3],["Misc Exhaust Gas Temperature",365,3],["Hydraulic Pump Rate",125,2]]
    self.high_df = pd.DataFrame(self.high, columns = ["Parameter","Threshold","Probability"])
    self.thresholds = [self.low_df,self.lowhigh_df,self.high_df]

  def reg(self,df) :
    model = LinearRegression()
    df["time"] = pd.to_datetime(df["time"])

    df["numDate"] = df["time"].map(pd.Timestamp.toordinal)

    x = df[["numDate"]]
    y = df[["value"]]

    model.fit(x, y)
    slope = model.coef_[0]
    if slope[0] == 0.0:
      slope[0] = 1

    intercept = model.intercept_
    name = df.values[0][3] + " " + df.values[0][4]
    current_table = self.low_df
    i = 0
    for table in self.thresholds:
      if name in table["Parameter"].values:
        current_table = table
        break
    i = current_table[current_table["Parameter"] == name].index[0]
    risk_val = 0
    if (current_table.shape[1] == self.lowhigh_df.shape[1]):
      threshold_low = current_table.values[i][1]
      threshold_high = current_table.values[i][2]
      risk_val = current_table.values[i][3]
    else:
      threshold = current_table.values[i][1]
      risk_val = current_table.values[i][2]
    flag = 0
    if slope[0] >= 0:
      if(current_table.shape[0] == 4):
        threshold = threshold_high
      elif(current_table.equals(self.low_df)):
        flag = 1
      else:
        threshold = threshold
    else:
      if(current_table.shape[0] == 4):
        threshold = threshold_low
      elif(current_table.equals(self.high_df)):
        flag = 1
      else:
        threshold = threshold

    if(flag == 0):
      date_pred = round((threshold - intercept[0]) / slope[0])
      proper_date = datetime.date.fromordinal(date_pred)
    else:
      proper_date = datetime.date(2024, 8, 20)
      risk_val = 0
    proper_date = pd.to_datetime(proper_date)
    proper_date = pd.Timestamp.toordinal(proper_date)
    current_date = pd.Timestamp.toordinal(pd.to_datetime(datetime.date.today()))
    num_days = proper_date - current_date

    if risk_val == 0:
      statement = "Your " + name + " is perfectly fine!"
    elif num_days <= 0:
      statement = "Your " + name + " is in danger zone. Kindly visit your local service centre as soon as possible."
    else:
      statement = "Your " + name + " will get damaged in about " + str(num_days) + " days."
    
    return statement 
  
  

# handle zero risk case
# handle single data entry case

  def make_groups(self,df):
    grouped_dfs = []
    grouped = df.groupby(['id', 'machine', 'component', 'parameter'])
    for group_name, group_df in grouped:
      grouped_dfs.append(group_df.reset_index(drop=True))
    return grouped_dfs

  def predict(self,json_data):
    df = pd.DataFrame(json_data)
    solList = []
    for group in self.make_groups(df):
      solList.append(self.reg(group))
    return solList
