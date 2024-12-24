from dataclasses import dataclass

@dataclass
class ModelRequest:
    model:str
    prompt:str
    stream:bool
