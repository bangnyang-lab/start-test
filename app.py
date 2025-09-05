import streamlit as st
import pandas as pd

st.set_page_config(page_title="템 획득 경로 백과사전", layout="centered")
st.title("템 획득 경로 백과사전")
st.write("아이템 이름(전체/일부)을 입력하면 관련 아이템을 보여줍니다.")

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

# 뒤로가기 버튼
if st.button("뒤로가기"):
    search_results = go_back()
else:
    search_results = search(query_input) if query_input else None

# 자동완성 + 드롭다운 방식
if search_results is not None and not search_results.empty:
    matches = search_results["name"].tolist()
    selected_item = st.selectbox("검색 결과:", matches)
    
    # 선택된 아이템 상세 정보
    item_data = df[df["name"] == selected_item].iloc[0]
    st.write(f"**{selected_item} 획득 경로**")
    for col in df.columns[1:]:
        value = str(item_data[col]).strip()
        if value == "✅":
            st.write(f"- {col}")
elif query_input:
    st.warning("검색 결과가 없습니다.")
