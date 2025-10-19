from pydantic import BaseModel


class Greetbody(BaseModel):
    name: str
