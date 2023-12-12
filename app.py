from video import *
import streamlit as st
from streamlit.components.v1 import html

flow=[]

stream(flow)

c=st.button('Clear',key=1)
s=st.button('Say',key=2,on_click=say(flow))

# st.markdown(
#     '''
# <button onclick="func()">Say</button>
# ''',unsafe_allow_html=True
# )

htmlScript="""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>

<body>
    <audio controls id="hello" src="./test.mp3" hidden></audio>
</body>
<script>
    var x = document.getElementById('hello');
    function func() {
        x.play();
    }
</script>

</html>
"""





if c:
    flow=[]
    c=False

elif s:
    say(flow)
    s=False

html(htmlScript)