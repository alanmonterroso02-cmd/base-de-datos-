from pydantic import BaseModel

class RecicladorLoginResponse(BaseModel):
    token: str
