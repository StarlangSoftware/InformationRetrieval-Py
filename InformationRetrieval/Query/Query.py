from Dictionary.Word import Word


class Query:

    __terms: [Word]

    def __init__(self, query: str):
        self.__terms = []
        terms = query.split(" ")
        for term in terms:
            self.__terms.append(Word(term))

    def getTerm(self, index: int) -> Word:
        return self.__terms[index]

    def size(self) -> int:
        return len(self.__terms)
