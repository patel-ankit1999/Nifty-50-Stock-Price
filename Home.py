import streamlit as st
import pandas as pd
from datetime import date
import time
from datetime import datetime
from plotly import graph_objs as go

st.title('Nifty 50 Stock Price Forecasting')




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

data = dataset()

st.subheader('Historical Data')
st.write(data.tail(10))


# EDA

st.subheader('Trend Analysis')

def plot_historical_data():

	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

plot_historical_data()
    




    


