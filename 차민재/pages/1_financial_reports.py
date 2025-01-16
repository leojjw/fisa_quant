import sys
from pathlib import Path

import pandas as pd
import streamlit as st

sys.path.append(str(Path(__file__).resolve().parent.parent))

from fs_global import fs as fs_global
from fs_domestic import fs_domestic 

st.set_page_config(layout="wide")

# 사이드바 설정
st.sidebar.title("Financial Reports")

# "검색 초기화하기" 버튼 클릭 시 모든 상태 초기화
if st.sidebar.button("검색 초기화하기"):
    st.session_state.clear()

# 종목 코드 입력
if 'ticker' not in st.session_state:
    st.session_state['ticker'] = ""  # 초기화

ticker = st.sidebar.text_input("종목코드를 입력해주세요", st.session_state['ticker'])

# 실적 옵션 상태 관리
if 'view_option' not in st.session_state:
    st.session_state['view_option'] = "분기실적"  # 기본값: 분기실적

# 데이터 상태 관리
if 'financial_data' not in st.session_state:
    st.session_state['financial_data'] = None  # 초기화

# 재무제표 조회 버튼
if st.sidebar.button("재무제표 조회하기"):
    # ticker가 숫자일 경우 한국 종목 코드 처리
    if ticker.isdigit():  # 한국 종목
        df = fs_domestic(ticker)
    else:
        # 재무제표 데이터 가져오기
        df = fs_global(ticker)

    if df is not None:
        st.session_state['financial_data'] = df  # 데이터를 상태에 저장
    else:
        st.sidebar.warning("재무제표를 조회할 수 없습니다. 종목 코드를 다시 확인해 주세요.")

# 데이터가 존재하는 경우만 표시
if st.session_state['financial_data'] is not None:
    # 실적 보기 옵션 (라디오 버튼)
    st.session_state['view_option'] = st.sidebar.radio(
        "실적 보기 옵션을 선택하세요:",
        options=["분기실적", "연간실적"],
        index=0 if st.session_state['view_option'] == "분기실적" else 1,
    )

    # 선택한 실적 옵션에 따라 데이터 필터링
    df = st.session_state['financial_data']
    if st.session_state['view_option'] == "연간실적":
        filtered_df = df.iloc[:, :3]  # 연간실적 데이터
    else:
        filtered_df = df.iloc[:, -3:]  # 분기실적 데이터

    # 변화량 계산
    if filtered_df.shape[1] > 1:  # 변화량 계산할 이전 데이터가 있는 경우
        latest_values = filtered_df.iloc[:, -1]  # 마지막 컬럼 값
        previous_values = filtered_df.iloc[:, -2]  # 바로 이전 컬럼 값
        changes = latest_values - previous_values  # 변화량

        # 변화량 테이블 준비
        results = pd.DataFrame({
            "항목": filtered_df.index,
            "최신 값": latest_values.values,
            "변화량": changes.values
        })

        # 변화량에 따라 색상 지정
        def format_changes(row):
            if row["변화량"] > 0:
                return f"<span style='color:red;'>+{row['변화량']:,}</span>"  # 빨간색
            elif row["변화량"] < 0:
                return f"<span style='color:blue;'>{row['변화량']:,}</span>"  # 파란색
            else:
                return f"{row['변화량']:,}"  # 기본값

        # 변화량 컬럼에 색상 적용
        results["변화량"] = results.apply(format_changes, axis=1)

        # 두 열로 나누어 표시
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("최근 데이터와 변화량")
            st.write(
                results.to_html(escape=False, index=False),
                unsafe_allow_html=True
            )

        with col2:
            st.subheader("재무제표")
            st.dataframe(filtered_df)
    else:
        st.warning("변화량을 계산할 이전 데이터가 없습니다.")
