import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import mediapipe as mp
from gestures.init import *
from gestures.gestures import *
import pyttsx3 as ps

mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic()


dots = {'face': {}, 'lh': {}, 'rh': {}, 'pose': {}}

cap = cv2.VideoCapture(0)
i = st.empty()


def stream(flow: list):
    # logger = logging.getLogger(__name__)

    webrtc_ctx = webrtc_streamer(
        key="video-sendonly",
        mode=WebRtcMode.SENDONLY,
        media_stream_constraints={"video": True},
    )

    image_place = st.empty()
    buffer = st.empty()
    q = st.empty()
    c = st.empty()
    s = st.empty()
    i = 1
    st.session_state['clear'] = 0
    st.session_state['say'] = 0
    st.session_state['quit'] = 0

    while True:
        if webrtc_ctx.video_receiver:
            try:
                video_frame = webrtc_ctx.video_receiver.get_frame(timeout=1)
            except Exception as e:
                break

            img_rgb = video_frame.to_ndarray(format="rgb24")
            # imgRGB=cv2.cvtColor(img_rgb,cv2.COLOR_RGBA2RGB)
            img_rgb, results = mediapipe_detection(img_rgb, holistic)

            setDimension(img_rgb.shape)

            collectData(results, dots)

            try:
                if iLoveYou(dots):
                    printI(img_rgb, 'ILoveYou')
                    if flow == [] or flow[-1] != 'I Love You':
                        flow.append('I Love You')
                elif father(dots):
                    printI(img_rgb, 'Father')
                    if flow == [] or flow[-1] != 'Father':
                        flow.append('Father')
                if mother(dots):
                    printI(img_rgb, 'Mother')
                    if flow == [] or flow[-1] != 'Mother':
                        flow.append('Mother')
                elif house(dots):
                    printI(img_rgb, 'House')
                    if flow == [] or flow[-1] != 'House':
                        flow.append('House')
                elif hello(dots):
                    printI(img_rgb, 'Hello')
                    if flow == [] or flow[-1] != 'Hello':
                        flow.append('Hello')
                elif thanks(dots):
                    printI(img_rgb, 'Thanks')
                    if flow == [] or flow[-1] != 'Thanks':
                        flow.append('Thanks')
                else:
                    printI(img_rgb, ' ')

            except Exception as e:
                print('\n---------------------------')
                print(e)
                print('---------------------------\n')

            draw_landmarks(img_rgb, results)

            image_place.image(img_rgb)
        else:
            break

        buffer.text(str(flow))

engine=ps.init('sapi5')
engine.setProperty('voice',engine.getProperty('voices')[1].id)

def say(flow):
    engine.say('Hello, I am John.')
    engine.runAndWait()