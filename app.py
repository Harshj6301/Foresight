import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf

# Function to download data from yfinance
def download(ticker_symbol,start_date, end_date, interval='1m'):
    data = yf.download(ticker_symbol, interval = interval, start = start_date, end = end_date)
    print(data.info())
    return data
  
# Function for date input
def get_date_input(label):
    year = st.number_input(label='Year', min_value=2000, max_value=2100, key='year')
    month = st.number_input(label='Month', min_value=1, max_value=12, key='month')
    day = st.number_input(label='Day', min_value=1, max_value=31, key='day')
    return year, month, day

# Function to plot features x by y
def plot(var1, var2, data):    
    plt.figure(figsize=(12,5))
    #################
    plt.subplot(1,2,1)
    plt.plot(data[var1],data[var2], color='blue', alpha=0.7)

# Main function
def main():
    st.title('Decision Delta')
    
    # Add your logo/image
    logo = 'Assets/Logos/DecisionDeltaLogobyDesigner (1).png'
    st.image(logo, width=200,)
    ###########
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write(' ')
    with col2:
        st.image(logo,width=250)
    with col3:
        st.write(' ')
    
    #########
    st.subheader('Provide Data')

    ticker_name_input = st.text_input("Enter Ticker symbol")
    interval_input = st.text_input("Enter interval")

    st.subheader('Provide Start Date')
    Year_s, Month_s, day_s = get_date_input(label='Start Date')
    st.subheader('Provide End Date')
    Year_e, Month_e, day_e = get_date_input(label='End Date')

    start_date_input = datetime.date(int(Year_s), int(Month_s), int(day_s))
    end_date_input = datetime.date(int(Year_e), int(Month_e), int(day_e))

    # Add your download and plot functions here
    # For example:
    data = download(ticker_name_input, start_date_input, end_date_input, interval_input)
    plot(var1,var2,data)

if __name__ == "__main__":
    main()

