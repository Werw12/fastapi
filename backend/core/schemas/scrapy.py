from pydantic import BaseModel, HttpUrl

class ScrapyRequest(BaseModel):
    url: HttpUrl