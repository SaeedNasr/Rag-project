from enum import Enum

class LLMEnum(Enum):
    GPT3 = "gpt-3"
    GPT4 = "gpt-4"
    BERT = "bert"
    XLNET = "xlnet"
    ROBERTA = "roberta"


class OpenAiEnum(Enum):
    SYSYEM = "system"
    USER = "user"
    ASSISTANT = "assistant"