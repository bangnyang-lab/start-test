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

# 검색창
query_input = st.text_input("아이템 이름(전체/일부)을 입력하세요:")

# 뒤로가기 버튼
if st.button("뒤로가기"):
    results = go_back()
else:
    results = search(query_input) if query_input else None

# 결과 표시
if results is not None and not results.empty:
    st.subheader("검색 결과")
    for idx, row in results.iterrows():
        # 클릭하면 해당 아이템 검색
        if st.button(row["name"], key=row["name"]):
            results = search(row["name"])
            break

    selected_item = results.iloc[0]
    st.write(f"**{selected_item['name']} 획득 경로**")
    # ✅만 표시, 체크 안 된 경로는 아예 안 뜸
    for col in df.columns[1:]:
        value = str(selected_item[col]).strip()
        if value == "✅":
            st.write(f"- {col}")
elif query_input:
    st.warning("검색 결과가 없습니다.")
