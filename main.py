import streamlit as st
from enums import *
from dotenv import load_dotenv
from utils import *
from ChatPage import display as chat_display
from ConfigPage import display as config_display
from agent import create_guessinggame_agent
from dialogue import create_dialogue
from enums import *

def handle_selection_change():
    st.session_state.dialogue = create_dialogue()
    st.session_state.hyperparameters = init_hyperparameters(st.session_state.selected_model_type)
    st.session_state.game = create_guessinggame_agent(
        st.session_state.selected_game_type,
        st.session_state.selected_model_type,
        st.session_state.selected_turn_limit,
        st.session_state.hyperparameters,
        st.session_state.dialogue
    )
    st.session_state.needs_rerun = True  # 상태 변경 후 플래그 설정

def init_session_state():
    if "hyperparameters" not in st.session_state:
        st.session_state.hyperparameters = init_hyperparameters(st.session_state.selected_model_type)
    if "dialogue" not in st.session_state:
        st.session_state.dialogue = create_dialogue()
    if "game" not in st.session_state:
        st.session_state.game = create_guessinggame_agent(
            st.session_state.selected_game_type,
            st.session_state.selected_model_type,
            st.session_state.selected_turn_limit,
            st.session_state.hyperparameters,
            st.session_state.dialogue
        )
    if "needs_rerun" not in st.session_state:
        st.session_state.needs_rerun = False  # 플래그 초기화

        
def refresh():
    st.session_state.selected_model_type = ModelType.list()[0]
    st.session_state.selected_turn_limit = TurnLimit.list()[0]
    st.session_state.selected_game_type = GameType.list()[0]
    handle_selection_change()

st.session_state.selected_model_type = st.sidebar.selectbox("Choose an option", ModelType.list(), index=0, on_change=handle_selection_change)
st.session_state.selected_turn_limit = st.sidebar.selectbox("Choose an option", TurnLimit.list(), index=0, on_change=handle_selection_change)
st.session_state.selected_game_type = st.sidebar.selectbox("Choose an option", GameType.list(), index=0, on_change=handle_selection_change)
st.sidebar.button("Reset", on_click=refresh)

# 메인 코드 블록에서 플래그 확인 후 rerun
if st.session_state.get("needs_rerun", False):
    st.session_state.needs_rerun = False  # 플래그 초기화
    st.rerun()

st.sidebar.title("Page")
page_options = ["Test Page", "Config Page"]
selected_page = st.sidebar.selectbox("Select a Page", page_options)

load_dotenv()
init_session_state()

if selected_page == "Test Page":
    chat_display()
elif selected_page == "Config Page":
    config_display()