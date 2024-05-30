from typing import Dict, Any
from openai import OpenAI
from anthropic import Anthropic
import random
import re

class Dialogue:
    def __init__(self, limit_turns : int = None):
        self.messages = []
        self.parameter_messages = []
        self.limit_turns = limit_turns * 2 if limit_turns else 10000
        
    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})
        if len(self.parameter_messages) > self.limit_turns:
            self.parameter_messages = self.parameter_messages[2:]
        self.parameter_messages.append({"role": role, "content": content})
        
    def clear_messages(self):
        self.messages = []
        
    def get_history(self):
        return self.messages
    
    def get_parameter_history(self):
        return self.parameter_messages
        
    def size(self):
        return len(self.messages)
    
    def isEmpty(self):
        return True if self.size() == 0 else False
    
    def set_limit_turn(self, limit_turn):
        self.limit_turns = limit_turn * 2

class Caller:
    def __init__(self, api_caller_object, model_type: str):
        self.api_caller_object = api_caller_object
        self.model_type = model_type
        
    def inference(self, hyperparameters: Dict[str, Any], dialouge_history : Dialogue, system_prompt: str):
        if isinstance(self.api_caller_object, OpenAI):
            return self.api_caller_object.chat.completions.create(
                    model=self.model_type,
                    messages=[{"role": "system", "content": system_prompt}] + dialouge_history.get_parameter_history(),
                    **hyperparameters
                ).choices[0].message.content
        elif isinstance(self.api_caller_object, Anthropic):
            return self.api_caller_object.chat.completions.create(
                model=self.model_type,
                system=system_prompt,
                messages=dialouge_history.get_parameter_history(),
                **hyperparameters
            ).choices[0].message.content
        else:
            raise ValueError("Invalid model type")

class WordPool:
    def __init__(self):
        self.word_list = load_file("resource/words.md").split("\n")
        
    def get_random_word(self):
        return random.choice(self.word_list)

class GeussingGame_field:
    def __init__(self, caller: Caller, limit_turn: int, hyperparameters: Dict[str, Any], dialouge_history: Dialogue):
        self.caller = caller
        self.hyperparameters = hyperparameters
        self.dialouge_history = dialouge_history
        self.dialouge_history.set_limit_turn(limit_turn)
        self.pipeline = [self.pre_process, self.call_inference, self.post_process]
        self.origin_system_prompt = load_file("resource/system_prompt.md")
        self.word_pool = WordPool()
        self.system_prompt = None
        self.answer = None
        self.isEnded = False
        self.start_game()

    def start_game(self):
        self.answer = self.word_pool.get_random_word()
        self.system_prompt = self.origin_system_prompt.replace("{content}", self.answer)

    def get_current_answer(self):
        return self.answer

    def talk(self, prompt: str = None):
        result = (prompt, True)
        for step in self.pipeline:
            result = step(*result)
            if result[1] == None or result[1] == False:
                return result[0]
        return result

    # 파이프라인 로직
    # 파이프라인 callback에서는 input으로 string이 정의되어야 함
    # 파이프라인 callback에서는 output으로 string이 정의되어야 함
    def pre_process(self, prompt: str, is_going: bool):
        if is_going == False:
            return (prompt, is_going)
        if self.isEnded == True:
            return ("The game is ended. Please, click the 'refresh' button on the left side.", False)
        if self.dialouge_history.size() >= 41:
            return ("You missed the game. Please, try again. click the 'refresh' button on the left side.", False)
        else:
            return (prompt, is_going)

    def call_inference(self, prompt: str, is_going: bool):
        if is_going == False:
            return (prompt, is_going)
        if check_is_answer_in_prompt(prompt, self.answer) == True:
            self.isEnded = True
            correct_message = f"Yes! You are correct. the answer is {self.answer}"
            self.dialouge_history.add_message("user", prompt)
            self.dialouge_history.add_message("assistant", correct_message)
            return (prompt, False)
        self.dialouge_history.add_message("user", prompt)
        response = self.caller.inference(
            self.hyperparameters,
            self.dialouge_history,
            self.system_prompt
        )
        self.dialouge_history.add_message("assistant", response)
        return (response, is_going)

    def post_process(self, response: str, is_going: bool):
        if is_going == False:
            return (response, False)
        return (response, None)# 후처리 로직을 여기에 추가

class Heejin_GeussingGame_field(GeussingGame_field):
    def __init__(self, caller: Caller, limit_turn: int, hyperparameters: Dict[str, Any], dialouge_history: Dialogue):
        super().__init__(caller, limit_turn, hyperparameters, dialouge_history)
        self.hints = self.generate_20_hints()
        
    def generate_20_hints(self):
        import json
        system_prompt = load_file("resource/heejin_hints.md")
        system_prompt = system_prompt.replace("{content}", self.answer)
        generated = self.caller.chat.completions.create(
            model=self.caller.model_type,
            messages=[{"role": "system", "content": system_prompt}]
        )
        hints = json.loads(generated)
        return hints["hints"]
    
    def talk(self, prompt: str = None):
        if check_is_answer_in_prompt(prompt, self.answer) == True:
            self.isEnded = True
            correct_message = f"Yes! You are correct. the answer is {self.answer}"
            self.dialouge_history.add_message("user", prompt)
            self.dialouge_history.add_message("assistant", correct_message)
            return (prompt, False)
        else:
            self.dialouge_history.add_message("user", prompt)
            response = f"No. that's not correct. Hint: {random.choice(self.hints)}"
            self.dialouge_history.add_message("assistant", response)
            return response 

def load_file(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def check_is_answer_in_prompt(prompt: str, answer: str):
    copy_prompt = str(prompt)
    spaced_prompt = re.sub(r'([a-zA-Z])([가-힣])', r'\1 \2', re.sub(r'([가-힣])([a-zA-Z])', r'\1 \2', copy_prompt))
    filtered_prompt = re.sub(r'[^가-힣a-zA-Z0-9\s]', '', spaced_prompt)
    word_list = filtered_prompt.split(" ")
    for word in word_list:
        if word == answer:
            return True
    return False
