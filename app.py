import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf
from duckduckgo_search import DDGS


# Function to download data from yfinance
@st.cache_data
def download(ticker_symbol,start_date, end_date, interval='1m'):
    data = yf.download(ticker_symbol, interval = interval, start = start_date, end = end_date)
    data = data.reset_index()
   # print(data.info())
    return data

# Function to fetch symbols from yfinance library
def fetch_symbols(url):
        symbols = []
        # Fetch HTML content from the URL
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find all rows containing symbols
            rows = soup.find_all('tr')
    
            # Extract symbols from each row
            for row in rows:
                symbol_td = row.find('td', class_='TAL')
                if symbol_td:
                    symbol_link = symbol_td.find('a')
                    if symbol_link:
                        symbol = symbol_link.text.strip()
                        symbols.append(symbol)
        return symbols

# news from ddg
def headlines(query, max_results):
  ddg = DDGS()
  result = ddg.news(query, region='us-en', max_results=max_results)
  # stripping and processing data
  final_result = []
  for i in result:
    final_result.append([i['title'], i['body'], i['source'], i['date']])
  return final_result

def search_symbol_name(query, max_results):
    ddg = DDGS()
    tks_fn = ddg.text(query, region='us-en', max_results=max_results)
    result = tks_fn[0]['title'].replace('- Yahoo Finance','')
    return result

def format_date(date):
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
    formatted_date = date_obj.strftime("%b %d %Y")
    return formatted_date

# Main function
def main():
    # Add your logo/image
    #logo = "Assets/Logos/bullai.png"
    name = "Assets/Name/Foresight.png"
    st.image(name, width=250)
   # st.title('Foresight')
    st.subheader('')
    st.subheader('ML and analytics for options', divider='rainbow')
    st.caption('_Please switch to wide mode for better viewing experience_')

    #########
    st.subheader('Provide Data')
    # Using selectbox or autocomplete thing for input
    
    # URL of the webpage containing F&O symbols
    url = 'https://www.moneycontrol.com/stocks/fno/marketstats/futures/most_active/homebody.php?opttopic=&optinst=allfut&sel_mth=all&sort_order=0'
    
    # Fetch symbols from the URL and remove duplicates
    fno_symbols = list(fetch_symbols(url))

    # Select Exchange
    exchange = st.radio('Select Exchange', ['NSE', 'FWB', 'JPX', 'LSE', 'HKG', 'NYSE'], 
                        captions=['India', 'Germany', 'Japan', 'London', 'China', 'US'], horizontal=True)
    
    # Other tickers
    selected_symbol = st.text_input("Enter Ticker symbol (For other tickers)")

    try:
        if exchange == 'NSE':
            selected_symbol = f"{selected_symbol}.NS"
        elif exchange == 'FWB':
            selected_symbol = f"{selected_symbol}.DE"
        elif exchange == 'JPX':
            selected_symbol = f"{selected_symbol}.T"
        elif exchange == 'HKG':
            selected_symbol = f"{selected_symbol}.HK"
        elif exchange == 'LSE':
            selected_symbol = f"{selected_symbol}.L"
    except:
        pass

    # Selected final ticker
    result = search_symbol_name(selected_symbol, max_results = 1)
    st.write('Selected Ticker:', result)

    ####################### 
    # Interval options for data download
    interval_options = st.selectbox("Enter interval",
                                    ('1m','5m','15m','1h','1d','1wk'))

    # UI for selecting start and end date to download data
    col1,col2 = st.columns(2)
    with col1:
        start_date_input = st.date_input('Provide Start Date', value=None)
    with col2:
        end_date_input = st.date_input('Provide End Date', datetime.datetime.now())

    # Divider line
    st.write('---')
    
    # Download data according to time frame
    data = download(selected_symbol, start_date_input, end_date_input, interval_options)
    
    # Data frame of downloaded data and headlines for the ticker (top 3)
    data_col, news_col = st.columns(2)
    with data_col:
        if st.checkbox("Show full data"):
            st.write(data)
        else:
            st.write(data.head())
    with news_col:
        st.write(':orange[Headlines]')
        news = headlines(result, max_results = 3) 
        for headline, description, source, date in news:
            st.markdown(headline)
            st.write(description)
            col1, col2 = st.columns(2)
            with col1:
                st.caption(f"Source: {source}")
            with col2:
                st.caption(format_date(date))

    # Divider line
    st.write('---')
    # plot feature selection
    col_1, col_2, col_3, col_4 = st.columns(4)
    with col_1:
        x_feature = st.selectbox("Select X Feature", data.columns, index=0, key=1)
    with col_2:
        y_feature = st.selectbox("Select Y Feature", data.columns, index=4, key=2)
    with col_3:
        x1_feature = st.selectbox("Select X Feature", data.columns, index=0, key=3)
    with col_4:
        y1_feature = st.selectbox("Select Y Feature", data.columns, index=6, key=4)
   # line chart
    col_1, col_2 = st.columns(2)
    with col_1:
        fig = px.line(data, x=x_feature, y=y_feature, title=f'{y_feature} vs {x_feature}')
        st.plotly_chart(fig)
    with col_2:
         fig = px.line(data, x=x1_feature, y=y1_feature, title=f'{y1_feature} vs {x1_feature}')
         st.plotly_chart(fig)
        
if __name__ == "__main__":
    main()


