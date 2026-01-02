from __future__ import annotations
from typing import List,Dict
from models.topic import Topic

class User:
    def __init__(self,username:str):
        self.username = username
        self.topics: List[Topic] = []

    def add_topic(self,topic:Topic) -> None:
        self.topics.append(topic)

    def to_dict(self) -> Dict:
        return {
            "username":self.username,
            "topics": [t.to_dict() for t in self.topics],
        }
    
    @classmethod
    def from_dict(cls,data: Dict) -> User:
        user = cls(data["username"])
        user.topics = [Topic.from_dict(t) for t in data.get("topics",[])]
        return user
    
    def __str__(self) -> str:
        return f"User({self.username})"
    