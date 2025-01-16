import FinanceDataReader as fdr
import FinanceDataReader.naver as fdrn

from datetime import datetime
import numpy as np
import pandas as pd

# 분기별 종료 날짜 계산 함수
def get_end_date(year, quarter):
    quarter_end_months = {1: "12-31", 2: "03-31", 3: "06-30", 4: "09-30"}
    if quarter == 1:
        return pd.to_datetime(f"{year-1}-{quarter_end_months[quarter]}")
    return pd.to_datetime(f"{year}-{quarter_end_months[quarter]}")

remain_columns =['매출액', '영업이익','당기순이익','자산총계', '부채총계', '자본총계','ROE(%)', 'ROA(%)', '부채비율','PER(배)','PBR(배)']

def fs_domestic(ticker) :
    today = datetime.now()

    # 최근 3개의 분기별 데이터 가져오기
    current_quarter = (today.month - 1) // 3 + 1
    quarter_df = fdrn.snap.finstate_summary(ticker, fin_type='0', freq='Q')

    quarter_df['Date'] = quarter_df.index # 인덱스 초기화
    quarter_df.reset_index(drop=True, inplace=True)

    end_date = get_end_date(today.year, current_quarter)
    quarter_df = quarter_df[quarter_df['Date'] <= end_date].tail(3)

    date_columns = quarter_df['Date'].dt.strftime('%Y-%m-%d')
    quarter_df = quarter_df[remain_columns]
    quarter_df = quarter_df.T
    quarter_df.columns = date_columns

    # 연간 데이터
    year_df = fdrn.snap.finstate_summary(ticker, fin_type='0', freq='Y')
    year_df['Date'] = year_df.index # 인덱스 초기화
    year_df.reset_index(drop=True, inplace=True)

    year = today.year - 1
    year_df = year_df[year_df['Date'].dt.year <= 2023].tail(3)

    date_columns = year_df['Date'].dt.strftime('%Y-%m-%d')
    year_df = year_df[remain_columns]
    year_df = year_df.T
    year_df.columns = date_columns

    df = pd.concat([year_df, quarter_df], axis =1)
    columns = pd.MultiIndex.from_tuples(
    [("연간", col) if idx < 3 else ("분기", col) for idx, col in enumerate(df.columns)]
    )
    df.columns = columns

    return df