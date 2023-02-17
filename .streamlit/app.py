import streamlit as st
import openai
import os
from functions import summarize

try:

    openai.api_key=os.getenv("OPENAI_KEY")

    if "summary" not in st.session_state:
    st.session_state["summary"] = ""

    st.title("Text Summarizer")

    input_text = st.text_area("Enter Text Here: ",value="", height=250)

    st.button("Summarize", on_click=summarize, kwargs={"prompt": input_text})

    output_text = st.text_area(label='Summary:', value=st.session_state["summary"], height=250)

except:
    st.write("Error")

