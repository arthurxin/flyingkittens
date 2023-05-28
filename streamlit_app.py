import streamlit as st
import pandas as pd
import numpy as np


st.markdown('Flyingkitten')

# 设置网页标题
st.title(' Immersive Storytelling ')

# 展示一级标题
st.header(u'Chapter1 Preface')

st.text('welcome to your story')

if st.button("start!"):
    "the story start in a dark night..."

st.text_area("Enter your behavior",''' What are you going to do? ''',
             height=200)

inference = st.text_input("Enput your inference", "calm")
st.write('The current inference is', inference)