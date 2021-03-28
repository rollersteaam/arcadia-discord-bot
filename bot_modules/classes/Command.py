class Command:
    def __init__(self, phrase: str, response: str):
        self.phrase = phrase
        self.response = response

    def match(self, response: str) -> bool:
        return self.response == response
