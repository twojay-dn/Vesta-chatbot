import streamlit as st
from dialogue import create_dialogue

def display():
    dialogue = st.session_state.dialogue
    is_start = True
    
    if is_start:
        add_to_dialogue("assistant", "Hello, let's start the game!")
        is_start = False

    prompt = st.chat_input("What is up?")
    if prompt:
        st.session_state.game.talk(prompt)
        
    display_dialogue(dialogue)
    display_game_answer()

def display_game_answer():
    if hasattr(st.session_state, 'game') and hasattr(st.session_state.game, 'answer'):
        st.markdown(f"**Current Answer:** {st.session_state.game.get_current_answer()}")
        st.markdown(f"**Current selected model:** {st.session_state.game.caller.model_type}")
        st.markdown(f"**Current selected game:** {st.session_state.selected_game_type.value}")
        
def add_to_dialogue(role, prompt):
    with st.chat_message(role):
        st.markdown(prompt)
        
def display_dialogue(dialogue):
    for message in dialogue.get_history():
        with st.chat_message(message.get("role")):
            st.markdown(message.get("content"))