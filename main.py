import streamlit as st
import pandas as pd
from io import StringIO
import os
st.title("Welcome to ETL Page")
def main():
    with st.sidebar:
        option = st.selectbox(
            'Upload the Files',
            ('Orders', 'Returns'))
        st.write("This code will be printed to the sidebar.")

    if option=="Orders":
        st.write('You selected:',"Orders")
        file = st.file_uploader("Upload Orders file", type=["csv", "png", "jpg","xlsx"])
        show_file = st.empty()

    if option=="Returns":
        st.write('You selected:',"Returns")
        file= st.file_uploader("Upload Returns file", type=["csv", "png", "jpg","xlsx"])
        show_file = st.empty()

    if not file:
        show_file.info("Please upload a file of type: " + ", ".join(["csv", "png", "jpg","xlsx"]))
        return

    else:
        data = pd.read_csv(file)
        st.dataframe(data.head(10))
    file.close()


main()










