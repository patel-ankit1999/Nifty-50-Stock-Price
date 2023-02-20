import streamlit as st
import pandas as pd
from datetime import date
import time
from datetime import datetime
import pandas_ta

st.title('Technical Analysis')

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
df['Date'] = pd.to_datetime(df['Date'])
df = df.set_index('Date')


def  Year_end_Frequency_of_Max_Price(df):
    st.header('Year End Frequency - Price')
    st.bar_chart(df.resample(rule='A').max()['Open'],  width=5)

Year_end_Frequency_of_Max_Price(df)

def  Year_end_Frequency_of_Volume(df):
    st.header('Year End Frequency - Volume')
    st.bar_chart(df.resample(rule='A').mean()['Volume'],width=5)

Year_end_Frequency_of_Volume(df)

def  Quarterly_Start_Frequency_of_Max_Price(df):
    st.header('Quarterly Strat Frequency - Price')
    st.line_chart(df.resample(rule='QS').max()['Open'], width=5)

Quarterly_Start_Frequency_of_Max_Price(df)

def Quarterly_Start_Frequency_of_Volume(df):
    st.header('Quarterly Strat Frequency - Volume')
    st.line_chart(df.resample(rule='QS').mean()['Volume'], width=5)

Quarterly_Start_Frequency_of_Volume(df)


def  Month_end_Frequency_of_Price(df):
    st.header('Month End Frequency - Price')
    st.bar_chart(df['Open'].resample(rule='M').mean(), width=5)

Month_end_Frequency_of_Price(df)

def Simple_Moving_Average(df):
    st.header('Simple Moving Average')
    
    df['Close_10_day_rolling'] = df['Close'].rolling(window=10, 
    min_periods=1).mean()
    df['Close_20_day_rolling'] = df['Close'].rolling(window=20, 
    min_periods=1).mean()
    df['Close_50_day_rolling'] = df['Close'].rolling(window=50, 
    min_periods=1).mean()
    st.line_chart(df[['Close_10_day_rolling','Close_20_day_rolling','Close_50_day_rolling','Close']], width=5)

Simple_Moving_Average(df)

def Cummulative_Moving_Average(df):
    st.header('Cummulative Moving Average')
    df['CMA_close'] = df['Close'].expanding().mean()
    st.line_chart(df[['CMA_close', 'Close']], width=5)

Cummulative_Moving_Average(df)

def Exponential_Moving_Average(df):
    st.header('Exponential Moving Average')
    df['EMA_10']=df.ta.ema(close='Close', length=10, append=True)
    df['EMA_20']=df.ta.ema(close='Close', length=20, append=True)
    df['EMA_30']=df.ta.ema(close='Close', length=30, append=True)
    df['EMA_50']=df.ta.ema(close='Close', length=50, append=True)
    st.line_chart(df[['EMA_10','EMA_20','EMA_30','EMA_50','Close']], width=5)
    
Exponential_Moving_Average(df)
    
    