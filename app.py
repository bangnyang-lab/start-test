import streamlit as st
import pandas as pd

st.set_page_config(page_title='템 획득 경로 백과사전', layout='centered')
df = pd.read_csv("items.csv", encoding='utf-8-sig')

st.title("템 획득 경로 백과사전")
st.write("아이템 이름(전체/일부)을 입력하면 관련 아이템을 보여줍니다.")

query = st.text_input("아이템 이름(전체/일부)을 입력하세요:")

if query:
    results = df[df['name'].str.contains(query, case=False, na=False)]
    if not results.empty:
        choice = st.selectbox("아이템을 선택하세요:", results["name"].tolist())
        item = results[results["name"] == choice].iloc[0]
        st.subheader(f"{choice} 획득 경로")
        for col in df.columns[1:]:
            v = item[col]
            st.write(f"- {col}: {'가능' if str(v).strip()!='' else '불가'}")
    else:
        st.warning("검색 결과가 없습니다.")
