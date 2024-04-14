import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf

# Function to download data from yfinance
@st.cache_data
def download(ticker_symbol,start_date, end_date, interval='1m'):
    data = yf.download(ticker_symbol, interval = interval, start = start_date, end = end_date)
    data = data.reset_index()
   # print(data.info())
    return data
  
# Function for date start input
def get_date_input_s(label):
    year = st.number_input(label='Year', min_value=2000, max_value=2100, key='year_s')
    month = st.number_input(label='Month', min_value=1, max_value=12, key='month_s')
    day = st.number_input(label='Day', min_value=1, max_value=31, key='day_s')
    return year, month, day
# Function for date end input
def get_date_input_e(label):
    year = st.number_input(label='Year', min_value=2000, max_value=2100, key='year')
    month = st.number_input(label='Month', min_value=1, max_value=12, key='month')
    day = st.number_input(label='Day', min_value=1, max_value=31, key='day')
    return year, month, day


# Function to plot features x by y
def plot(var1, var2, data):    
    plt.figure(figsize=(12,5))
    plt.plot(data[var1],data[var2], color='blue', alpha=0.7)

# Main function
def main():
    # Add your logo/image
    logo = 'Assets/Logos/DecisionDeltaLogobyDesigner (1).png'
    st.markdown("""
    <div style="text-align: center">
    <img src=logo alt="Logo" style="width: 200px;">  <h1>Decision Delta</h1>
    </div> """)
    
   
    #st.image(logo, width=200,)
    ###########
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(logo,width=250)
    with col3:
        st.write(' ')
        
    st.title('Decision Delta')
    st.subheader('Making decisions with precision and agility, for options trading', divider='rainbow')
    
  
    
    #########
    st.subheader('Provide Data')

    ticker_name_input = st.text_input("Enter Ticker symbol")
    #interval_input = st.text_input("Enter interval")
    interval_options = st.selectbox("Enter interval",
                                    ('1m','5m','15m','1h','1d','1wk'))
    
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('Provide Start Date')
        Year_s, Month_s, day_s = get_date_input_s(label='Start Date')
    with col2:
        st.subheader('Provide End Date')
        Year_e, Month_e, day_e = get_date_input_e(label='End Date')

    start_date_input = datetime.date(int(Year_s), int(Month_s), int(day_s))
    end_date_input = datetime.date(int(Year_e), int(Month_e), int(day_e))

    # Add your download and plot functions here
    if st.button("Run"):
        data = download(ticker_name_input, start_date_input, end_date_input, interval_options)
        st.write(data)
        # Plotly chart
        fig = px.line(data, x='Datetime', y='Close')
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()


