import streamlit as st
import speech_recognition as sr
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from elevenlabs import voices, generate, play,set_api_key
set_api_key(st.secrets['ELEVENLABS_API_KEY'])

voices_data = voices()
selectedVoice = voices_data[0]

template: str = """You are voice assistant named 'Voice Genius'. \
        You will answer the text that \
        is delimited by triple backticks \
        text: ```{text}``` \
    """

prompt_template = ChatPromptTemplate.from_template(template)
print(prompt_template)
llm_model: str = "gpt-3.5-turbo-1106"
llm = ChatOpenAI(model=llm_model,openai_api_key=st.secrets['OPENAI_API_KEY'])

def speech_to_text():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            return text
        except:
            text = 'Sorry could not recognize your voice'

def chat_with_llm(text: str) -> str:
    prompt = prompt_template.format_messages(text=text)
    response = llm(prompt)
    return response.content

def text_to_speech(text:str,voiceToUse):
    print("Generating audio...",text)
    print("Voice to use:",voiceToUse)
    audio = generate(text,voice=voiceToUse)
    play(audio)

st.title("Voice Genius")

st.write("This is a demo of the Voice Genius app. It is a work in progress.")

st.write("To get started, click the button below to record your voice.")

if('button_message' not in st.session_state):
    st.session_state['button_message']="Wanna talk?"

if('messages' not in st.session_state):
    st.session_state['messages'] = []

record_btn = st.button(st.session_state['button_message'])

st.session_state['status']=''
if record_btn:
    st.session_state['button_message'] = "Recording..."
    st.session_state['status'] = 'Recording...'
    text = speech_to_text()
    if text:
        st.session_state['messages'].append({
            'role': 'user',
            'message': text
        })
        st.session_state['status'] = 'Thinking...'
        response = chat_with_llm(text)
        st.session_state['messages'].append({
            'role': 'assistant',
            'message': response
        })
        text_to_speech(response,selectedVoice)
    else:
        st.session_state['messages'].append(
            {
                'role': 'assistant',
                'message':"Sorry, I couldn't hear you."
            })
        text_to_speech("Sorry, I couldn't hear you.",selectedVoice)
    st.session_state['status'] = ''
    st.session_state['button_message'] = "Ready to go?"
    

st.write(st.session_state['status'])

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.markdown(message['message'])