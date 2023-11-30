from video import *
import streamlit as st

flow=[]

stream(flow)

c=st.button('Clear',key=1)
s=st.button('Say',key=2)

if c:
    flow=[]
    c=0

elif s:
    say(flow)
    s=0
