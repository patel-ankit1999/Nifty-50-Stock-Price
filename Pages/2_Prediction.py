import streamlit as st
import pandas as pd
from datetime import date
import time
from datetime import datetime
import numpy as np


st.title('Prediction')




def dataset():
    
    #Reading stock list
    df_stocks = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv")

    stock = []
    for i in df_stocks['Symbol']:
        stock.append(i)
        
    stock = tuple(stock)
    select_stocks = st.selectbox('Select dataset for prediction', stock)
    

    #End date
    today = date.today()
    enddate = time.mktime(today.timetuple())
    enddate = str(int(enddate))

    # Start date
    startdate = datetime.now().date().replace(year=2019, month=2, day=17)
    stdate=time.mktime(startdate.timetuple())
    stdate=str(int(stdate))


    # Loading data
    def  load_data(ticker) :
        url = "https://query1.finance.yahoo.com/v7/finance/download/" +ticker+".NS?period1=" + stdate+ "&period2=" + enddate+ "&interval=1d&events=history&includeAdjustedClose=true"
        df = pd.read_csv(url)
        return df
    data = load_data(select_stocks)
    return data

df = dataset()

import requests
import pandas as pd
from datetime import date
import time
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import pandas_ta
import numpy as np

df_stocks = pd.read_csv("https://archives.nseindia.com/content/indices/ind_nifty50list.csv")
today  = date.today()
enddate = time.mktime(today.timetuple())
enddate = str(int(enddate))
startdate = datetime.now().date().replace(year=2019, month=2, day=17)
stdate=time.mktime(startdate.timetuple())
stdate=str(int(stdate))
stock = 'ADANIENT'
url = "https://query1.finance.yahoo.com/v7/finance/download/" +stock+ ".NS?period1=" + stdate+ "&period2=" + enddate+ "&interval=1d&events=history&includeAdjustedClose=true"
df = pd.read_csv(url)
df2 = df.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume'], axis=1)
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')
df1 = df[['Close']]
from sklearn.preprocessing import MinMaxScaler
MinMax = MinMaxScaler()
df1 = MinMax.fit_transform(df1)
training_size = int(len(df1)*0.70)
test_size = len(df1)-training_size 
train_data = df1[0:training_size,:]
test_data = df1[training_size :len(df1), :1]
def create_dataset(dataset, time_step=1):
    X,Y = [], []
    for i in range(len(dataset)-time_step-1):
        a = dataset[i:(i+time_step), 0]   
        X.append(a)
        Y.append(dataset[i + time_step, 0])
    return np.array(X), np.array(Y)
X_train, Y_train = create_dataset(train_data, 100)
X_test, Y_test = create_dataset(test_data, 100)
X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
model=Sequential()
model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
model.add(LSTM(50,return_sequences=True))
model.add(LSTM(50))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=100,batch_size=64,verbose=1)
train_predict=model.predict(X_train)
test_predict=model.predict(X_test)
scaler = MinMax.scale_
scale_factor = 1/scaler[0]
y_predicted = test_predict * scale_factor

y_test = Y_test* scale_factor


# Plotting graph
st.subheader("Predictions vs Original")
fig= plt.figure(figsize = (12,6))
plt.plot(Y_test, label = 'Original Price')
plt.plot(test_predict, label = 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig)
