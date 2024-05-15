from typing import Union

from pydantic import BaseModel


class ChannelUser(BaseModel):
    name: str
    waId: str
    msgId: str
    timestamp: int


class TemplateDynamicBody(BaseModel):
    type: Union[str, None] = None
    payload: Union[dict, None] = None
    renderPayload: Union[dict, None] = None


class HookArgs(BaseModel):
    channelUser: ChannelUser
    userInput: Union[str, None] = None
    flow: Union[str, None] = None
    additionalData: Union[dict, None] = None
    templateDynamicBody: Union[TemplateDynamicBody, None] = None
    methodArgs: Union[dict, None] = None
