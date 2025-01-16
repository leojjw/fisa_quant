import pandas as pd
import yfinance as yf


def fs(ticker):
    apple = yf.Ticker(ticker)
    apple

    af1 = apple.financials.loc[['Total Revenue', 'Operating Income', 'Net Income'], :]#['2022-09-30', '2023-09-30', '2024-09-30']]
    af1 = af1.iloc[:,:3]
    af1 = af1.iloc[:,::-1]
    af2 = apple.quarterly_financials.loc[['Total Revenue', 'Operating Income', 'Net Income'], :]# ['2024-03-31', '2024-06-30', '2024-09-30']]
    af2 = af2.iloc[:,:3]
    af2 = af2.iloc[:,::-1]
    af = pd.concat([af1, af2], axis=1)

    abs = apple.balance_sheet.loc[['Total Assets', 'Total Liabilities Net Minority Interest'], :]# ['2022-09-30', '2023-09-30', '2024-09-30']]
    abs = abs.iloc[:,:3]
    abs = abs.iloc[:,::-1]
    abs = abs.T
    abs['자본총계'] = abs['Total Assets'] - abs['Total Liabilities Net Minority Interest']
    abs = abs.T

    absq = apple.quarterly_balance_sheet.loc[['Total Assets', 'Total Liabilities Net Minority Interest'], :]# ['2024-03-31', '2024-06-30', '2024-09-30']]
    absq = absq.iloc[:,:3]
    absq = absq.iloc[:,::-1]
    absq = absq.T
    absq['자본총계'] = absq['Total Assets'] - absq['Total Liabilities Net Minority Interest']
    absq = absq.T

    ab = pd.concat([abs, absq], axis=1)

    r = pd.concat([af, ab]).T.astype(int)
    r['ROA(%)'] = round(r['Net Income'] / r['Total Assets'] * 100, 1)
    r['ROE(%)'] = round(r['Net Income'] / r['자본총계'] * 100, 1)
    r['부채비율'] = round(r['Total Liabilities Net Minority Interest'] / r['자본총계'] * 100, 2)
    r['PER(배)'] = round(apple.info['marketCap'] / r['Net Income'], 2)
    r['PBR(배)'] = round(apple.info['marketCap'] / r['Total Assets'], 2)
    r.columns = ['매출액', '영업이익','당기순이익','자산총계', '부채총계', '자본총계', 'ROE(%)', 'ROA(%)', '부채비율','PER(배)','PBR(배)']
    r = r.T
    column_list = r.columns
    multi_index = pd.MultiIndex.from_tuples(
        [("연간", column_list[0].strftime('%Y-%m-%d')), ("연간", column_list[1].strftime('%Y-%m-%d')), ("연간", column_list[2].strftime('%Y-%m-%d')),
        ("분기", column_list[3].strftime('%Y-%m-%d')), ("분기", column_list[4].strftime('%Y-%m-%d')), ("분기", column_list[5].strftime('%Y-%m-%d'))]
    )
					
# 컬럼에 멀티인덱스 적용
    r.columns = multi_index
    return r