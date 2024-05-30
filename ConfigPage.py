import streamlit as st

def display():
    st.title("Config")
    
    if st.session_state.get("hyperparameters"):
        st.write(st.session_state.get("hyperparameters"))
    else:
        st.write("No hyperparameters")
    
    # edit temperature
    new_temperature = st.slider(
        "temperature", 0.0, 1.0, st.session_state["hyperparameters"]["temperature"]
    )
    if new_temperature != st.session_state["hyperparameters"]["temperature"]:
        st.session_state["hyperparameters"]["temperature"] = new_temperature
        st.rerun()
    
    # edit top_p
    new_top_p = st.slider(
        "top_p", 0.0, 1.0, st.session_state["hyperparameters"]["top_p"]
    )
    if new_top_p != st.session_state["hyperparameters"]["top_p"]:
        st.session_state["hyperparameters"]["top_p"] = new_top_p
        st.rerun()
    
    # edit frequency_penalty
    new_frequency_penalty = st.slider(
        "frequency_penalty", 0.0, 1.0, st.session_state["hyperparameters"]["frequency_penalty"]
    )
    if new_frequency_penalty != st.session_state["hyperparameters"]["frequency_penalty"]:
        st.session_state["hyperparameters"]["frequency_penalty"] = new_frequency_penalty
        st.rerun()
    
    # edit presence_penalty
    new_presence_penalty = st.slider(
        "presence_penalty", 0.0, 1.0, st.session_state["hyperparameters"]["presence_penalty"]
    )
    if new_presence_penalty != st.session_state["hyperparameters"]["presence_penalty"]:
        st.session_state["hyperparameters"]["presence_penalty"] = new_presence_penalty
        st.rerun()
        
    new_max_tokens = st.number_input(
        "max_tokens", 0, 1000, st.session_state["hyperparameters"]["max_tokens"]
    )
    if new_max_tokens != st.session_state["hyperparameters"]["max_tokens"]:
        st.session_state["hyperparameters"]["max_tokens"] = new_max_tokens
        st.rerun()
