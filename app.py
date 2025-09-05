import streamlit as st
import pandas as pd

st.set_page_config(page_title="템 획득 경로 백과사전", layout="centered")
st.title("이거 어떻게 얻음?")
st.write("아이템 이름(전체/일부)을 입력하면 관련 아이템을 보여줍니다.")

# 뒤로가기 버튼
if st.button("뒤로가기"):
    search_results = go_back()
else:
    search_results = search(query_input) if query_input else None

# CSV 불러오기
df = pd.read_csv("items.csv", encoding='utf-8-sig')

# 검색 기록 스택
if "history" not in st.session_state:
    st.session_state.history = []

def search(query):
    if not query:
        return None
    if len(st.session_state.history) == 0 or st.session_state.history[-1] != query:
        st.session_state.history.append(query)
    results = df[df["name"].str.contains(query, case=False, na=False)]
    return results

def go_back():
    if len(st.session_state.history) > 1:
        st.session_state.history.pop()
        prev_query = st.session_state.history[-1]
        return search(prev_query)
    else:
        st.warning("더 이상 이전 검색 결과가 없습니다.")
        return None

# 검색창 입력
query_input = st.text_input("아이템 이름 입력:")

# 자동완성 + 드롭다운 방식
if query_input:
    # 입력값이 포함된 아이템 이름 리스트 만들기 (부분 일치)
    matches = df[df["name"].str.contains(query_input, case=False, na=False)]["name"].tolist()
    
    if matches:
        # 선택 가능 드롭다운
        selected_item = st.selectbox("연관 검색어:", matches)
        
        # 선택된 아이템 정보 표시
        item_data = df[df["name"] == selected_item].iloc[0]
        st.write(f"**{selected_item} 획득 경로**")
        for col in df.columns[1:]:
            if str(item_data[col]).strip() == "✅":
                st.write(f"- {col}")
    else:
        st.warning("검색 결과가 없습니다.")
