import streamlit as st
from enums import ModelType

def init_hyperparameters(model_type : ModelType):
    model_key = model_type.value.lower()[:3]
    match model_key:
        case "gpt":
            return {
                "temperature": 0.5,
                "top_p": 1.0,
                "frequency_penalty": 0.0,
                "presence_penalty": 0.0,
                "max_tokens": 200
            }
        case _:
            raise ValueError("Invalid model type")

def clear_messages():
    st.session_state["messages"] = []
