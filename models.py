from pydantic import BaseModel

class RuleModel(BaseModel):
    mailbox: str
    LINE_TOKEN: str
    send_body: bool = True

