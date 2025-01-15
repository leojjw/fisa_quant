import streamlit as st
import FinanceDataReader as fdr
import pandas as pd
# import talib
import streamlit.components.v1 as components
import datetime
from fs import *
# 대표 사이트 명
st.title(':달러: 우리FISA 증권 :달러:')
# Streamlit 제목 설정
st.title(':안내데스크_직원::피부톤-2: 실시간 주식 종목 분석')
# 사용자로부터 종목명, 종목코드 또는 티커 입력 받기
ticker = st.text_input(':단안경을_쓴_얼굴: 종목코드 또는 종목 티커를 입력하세요:', 'AAPL')
# TradingView 차트 삽입
st.subheader(':막대_차트: Technical Overview')
tradingview_widget = f"""
<iframe src="https://www.tradingview.com/widgetembed/?symbol={ticker}&theme=dark&style=1&timezone=Asia/Seoul&withdateranges=1&hide_side_toolbar=1&allow_symbol_change=1&save_image=1&studies=[]&locale=kr" width="100%" height="600" frameborder="0" allowfullscreen></iframe>
"""
components.html(tradingview_widget, height=400)
# FinanceDataReader를 사용하여 종목 데이터 가져오기
data = fdr.DataReader(ticker, start='2024-01-01')
# 실시간 주가 표시
st.subheader('실시간 주가')
st.write(f'현재가: {data.iloc[-1]["Close"]}')
st.write(f'전날 종가: {data.iloc[-2]["Close"]}')
st.write(f'최고가: {data["Close"].max()}')
st.write(f'최저가: {data["Close"].min()}')
# 과거 데이터 표시
st.subheader('종목 히스토리')
st.dataframe(data, width=1200)
# 실시간 매수/매도 및 공매도 데이터를 가져오는 함수 (예시: 수동 계산)
st.dataframe(bs1)
st.dataframe(is1)

def get_trade_data(ticker):
    # 예시로 FinanceDataReader를 사용하여 데이터를 가져옵니다.
    # 실제로는 거래소 API 등을 사용하여 매수/매도 데이터를 가져옵니다.
    data = fdr.DataReader(ticker, start='2024-01-01')
    return data
# 최근 한달간 매수/매도 및 공매도 데이터 가져오기
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=30)
trade_data = get_trade_data(ticker)
# 여기서는 주식 데이터만으로 매수/매도량을 계산할 수 있는 예시입니다.
# 실제 매수/매도량은 거래소 API 등을 사용하여 가져와야 합니다.
institution_buy = trade_data['Volume'].sum()  # 예시 데이터: 기관의 최근 한달간 총 매수량
institution_sell = trade_data['Volume'].sum() * 0.5  # 예시 데이터: 기관의 최근 한달간 총 매도량
individual_buy = trade_data['Volume'].sum() * 0.5  # 예시 데이터: 개인투자자의 최근 한달간 총 매수량
individual_sell = trade_data['Volume'].sum() * 0.4  # 예시 데이터: 개인투자자의 최근 한달간 총 매도량
short_selling = trade_data['Volume'].sum() * 0.1  # 예시 데이터: 공매도 현황
# 종합 분석
if institution_buy > institution_sell and individual_buy > individual_sell:
    opinion = '매수 의견'
    opinion_description = '기관과 개인 투자자 모두 최근 한달간 매수량이 매도량을 초과하므로, 해당 종목의 주식 가격 상승 가능성이 높다고 판단됩니다.'
elif institution_sell > institution_buy and individual_sell > individual_buy:
    opinion = '매도 의견'
    opinion_description = '기관과 개인 투자자 모두 최근 한달간 매도량이 매수량을 초과하므로, 해당 종목의 주식 가격 하락 가능성이 높다고 판단됩니다.'
else:
    opinion = '중립 의견'
    opinion_description = '기관과 개인 투자자의 매수량과 매도량이 비슷하므로, 해당 종목의 주식 가격이 변동 없이 안정적인 상태일 가능성이 높습니다.'
# 종합 분석 결과 표시
st.subheader('종합 분석 결과')
st.write(f'기관의 최근 한달간 총 매수량: {institution_buy}')
st.write(f'기관의 최근 한달간 총 매도량: {institution_sell}')
st.write(f'개인투자자의 최근 한달간 총 매수량: {individual_buy}')
st.write(f'개인투자자의 최근 한달간 총 매도량: {individual_sell}')
st.write(f'공매도 현황: {short_selling}')
st.write(f'현재 주식 가격에 대한 의견: {opinion}')
st.write(f'의견 설명: {opinion_description}')
# 인기 종목과 주가 변동성을 표로 표시
st.subheader('실시간 인기 종목 및 주가 변동성')
# 실시간 인기 종목 데이터 가져오기
krx = fdr.StockListing('KRX')
popular_stocks = krx.head(5)  # 상위 5개 종목 예시
# 인기 종목 실시간 데이터 가져오기 및 변동성 계산
popular_stocks_data = []
for code in popular_stocks['Code']:  # 'Symbol' 대신 'Code' 사용
    stock_data = fdr.DataReader(code, start='2023-01-01')
    current_price = stock_data.iloc[-1]['Close']
    prev_close = stock_data.iloc[-2]['Close']
    volatility = ((current_price - prev_close) / prev_close) * 100
    popular_stocks_data.append([code, current_price, prev_close, volatility])
# 데이터프레임 생성
popular_stocks_df = pd.DataFrame(popular_stocks_data, columns=['티커', '현재가', '전날종가', '변동성'])
# 표로 표시
st.table(popular_stocks_df)