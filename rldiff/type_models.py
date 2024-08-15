from datetime import datetime
from typing import Dict, Union
from pydantic import BaseModel
from rldiff.state import State
from rldiff.action import Action


class InfoDictionary(BaseModel):
    info: Dict[str, Union[State, Action, float, datetime]]
