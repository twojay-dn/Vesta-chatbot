from typing import Dict, Any
from openai import OpenAI
from Classes import GeussingGame_field, Caller, Dialogue, Heejin_GeussingGame_field
from enums import GameType, ModelType, TurnLimit
import os
        
def create_guessinggame_agent(
        gametype : GameType,
        model_type : str,
        limit_turn : TurnLimit,
        hyperparameters: Dict[str, Any],
        dialouge_history : Dialogue
    ):
    limit_turn = limit_turn.value
    match gametype:
        case GameType.NORMAL:
            return GeussingGame_field(
                caller=create_caller(model_type),
                limit_turn=limit_turn,
                hyperparameters=hyperparameters,
                dialouge_history=dialouge_history
            )
        case GameType.HEEJIN:
            return Heejin_GeussingGame_field(
                caller=create_caller(model_type),
                limit_turn=limit_turn,
                hyperparameters=hyperparameters,
                dialouge_history=dialouge_history
            )
        case _:
            raise ValueError("Invalid model type")
    
def create_caller(model_type : ModelType):
    sliced = model_type.value[:3]
    match sliced:
        case "gpt":
            api_caller = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            return Caller(api_caller, model_type.value)
        case _:
            raise ValueError("Invalid model type")
