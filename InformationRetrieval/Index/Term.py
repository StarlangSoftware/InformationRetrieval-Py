from Dictionary.Word import Word


class Term(Word):

    __term_id: int

    def __init__(self, name: str, termId: int):
        super().__init__(name)
        self.__term_id = termId

    def getTermId(self) -> int:
        return self.__term_id
