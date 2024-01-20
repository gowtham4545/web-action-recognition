import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import mediapipe as mp
from gestures.init import *
from gestures.gestures import *
from gtts import gTTS
import pyttsx3 as ps
from openai import OpenAI
import requests

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


engine = ps.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[1].id)


def say(flow):
    # engine.say('Hello, I am John.')
    # engine.save_to_file('Hello, I am John. Who are you.','test.mp3','hello')

    text = sentence(flow)

    obj = gTTS(text)
    obj.save('test.mp3')
    audio = open('test.mp3', 'rb').read()

    a = st.audio(audio)
    # engine.runAndWait()


def sentence(seq: list) -> str:
    KEY = requests.get('https://gowtham-api.vercel.app/keys').json()['key']
    client = OpenAI(api_key=KEY)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[

            {"role": "user", "content": "I will give some keywords and form a meaningful sentence from that"},
            {"role": "assistant", "content": "Of course, please provide me with the keywords, and I'll help you form meaningful sentences using them."},
            {"role": "user", "content": "i , innocent"},
            {"role": "assistant", "content": '''"I was falsely accused of a crime I didn't commit, but I knew in my heart that I was innocent."'''},
            {"role": "user", "content": '''not to generate a sentence which contains these keywords, just study the given keywords and give me the sentence'''},
            {"role": "assistant", "content": '''Understood, here's a sentence using the keywords "I" and "innocent":
"She insisted that I was innocent."'''},
            {"role": "user", "content": '''suppose a person is dumb and he cant speak, so he is making sentences via these keywors. He will give only nouns and verbs. generate sentence so that he can show that sentence to communicate with others '''},
            {"role": "assistant", "content": '''Certainly, if someone can only provide nouns and verbs to form sentences, here's an example of a sentence they could use to communicate:
"Dog chase cat."
In this simple sentence, "dog" is the subject (noun), and "chase" is the verb, indicating an action. "Cat" is the object (noun) of the action. This sentence conveys the idea that a dog is chasing a cat.'''},
            {"role": "user", "content": '''exactly, i will give those keywords to you, tell me what would be the sentence he is willing to communicate'''},
            {"role": "assistant", "content": '''Of course, please provide the nouns and verbs, and I'll help you form a sentence based on those keywords.'''},
            {"role": "user", "content": '''i, innocent'''},
            {"role": "assistant", "content": '''With the keywords "I" and "innocent," a simple sentence could be:
"I am innocent."
             Give me only the generated phrase and not the explanation'''},
            {"role": "user", "content": str(seq)}
        ]
    )
    sentence = response.choices[-1].message.content
    return sentence
