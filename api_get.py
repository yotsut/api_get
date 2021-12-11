import streamlit as st
import requests
import pandas as pd
import json

st.title('APIを一括発行するアプリ')
st.write("入力されたファイルに記載されたURLを順番にリクエストし、レスポンスを1ファイルにしてダウンロードします。")
st.write('・GETリクエストのみ。認証、リクエストボディの追加は非対応。レスポンスはJSONのみ。')
st.write('・入力ファイルは、ヘッダ無しで1行に1つのURL。拡張子はTXT or CSV')
uploaded_file = st.file_uploader("ファイルを入力するとスタートします。", type=['txt','csv'])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, names=['url']) #ヘッダー無し
    res_list = []
    progress_label = st.empty()
    bar = st.progress(0.0)
    for i, row in enumerate(df['url'].tolist()):
        res = requests.get(row)
        res_list.extend(res.json())
        progress_label.text(f'progress {i+1} / {len(df)}')
        bar.progress((i+1)/len(df))
    st.success("取得が完了しました。以下のボタンからダウンロードしてください。")
    st.download_button("Download file", json.dumps(res_list, ensure_ascii=False), file_name='response.json')
