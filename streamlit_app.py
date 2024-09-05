import streamlit as st
Lab1 = st.Page("lab1.py",title='Lab1')
Lab2 = st.Page("lab2.py",title='Lab2')
pg=st.navigation([Lab1,Lab2])
st.set_page_config(page_title='Lab Apps')
pg.run()