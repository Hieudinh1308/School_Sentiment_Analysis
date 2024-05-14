# Use a pipeline as a high-level helper
from transformers import pipeline
import streamlit as st
from PIL import Image



st.title("School Sentiment Analysis")

st.markdown('''
    :red[Type] :orange[something] :green[here]  .''')

model = pipeline("text-classification", model="hieudinhpro/BERT_Sentiment_Vietnamese")

text = st.text_area("")

predi_Bt = st.button("Predict")
if predi_Bt:
    predict = model (text)
    st.warning(predict)
    


