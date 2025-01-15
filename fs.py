import dart_fss as dart
import streamlit as st
import pandas as pd

# Open DART API KEY 설정
api_key='8229c7c5eb4a3b25e4edb3f8332d1ac68e15805f'
dart.set_api_key(api_key=api_key)

# DART 에 공시된 회사 리스트 불러오기
corp_list = dart.get_corp_list()

samsung = corp_list.find_by_corp_name('삼성전자', exactly=True)[0]

fs = samsung.extract_fs(bgn_de='20240101', report_tp='quarter')

bs = fs.show('bs')

bs1 = bs.droplevel(0, axis=1)
bs1 = bs1[(bs1.label_ko == '자산총계') | (bs1.label_ko == '자본총계') | (bs1.label_ko == '부채총계')]

bs1.columns = ['concept_id', 'label_ko', 'label_en', 'class0', 'class1', 'class2', 'class3', 'class4', \
                '20240930', '20240630', '20240331', '20231231', '20230930', '20230630', '20230331', '20221231', '20211231']
bs1 = bs1.set_index('label_ko')
bs1 = bs1.drop(columns=['20230930', '20230630', '20230331'])
bs1 = bs1.iloc[:,7:]

bs1 = bs1[['20211231', '20221231', '20231231', '20240331', '20240630', '20240930']]

multi_index = pd.MultiIndex.from_tuples(
    [("연간", "20211231"), ("연간", "20221231"), ("연간", "20231231"),
     ("분기", "20240331"), ("분기", "20240630"), ("분기", "20240930")]
)

# 컬럼에 멀티인덱스 적용
bs1.columns = multi_index
# st.write(bs1)
is_ = fs.show('is')
is1 = is_.droplevel(0, axis = 1)

is1 = is1[(is1.label_ko == '영업수익') | (is1.label_ko == '영업이익') | (is1.label_ko == '당기순이익(손실)')]
is1 = is1.set_index('label_ko')
is1 = is1.iloc[:,5:]
is1.columns = ['20240701-20240930', '20240401-20240630', '20240101-20240930', '20240101-20240630', '20240101-20240331'\
               ,'20230701-20230930', '20230401-20230630', '20230101-20231231', '20230101-20230930', '20230101-20230630'\
               ,'20230101-20230331', '20220101-20221231', '20210101-20211231']

is1 = is1[['20210101-20211231', '20220101-20221231', '20230101-20230331', '20240101-20240331', '20240401-20240630', '20240701-20240930']]
# st.write(is1)