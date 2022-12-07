from __future__ import annotations
from Dictionary.Word import Word


class Query:

    __terms: [Word]

    def __init__(self, query: str = None):
        self.__terms = []
        if query is not None:
            terms = query.split(" ")
            for term in terms:
                self.__terms.append(Word(term))

    def getTerm(self, index: int) -> Word:
        return self.__terms[index]

    def size(self) -> int:
        return len(self.__terms)

    def filterAttributes(self,
                         attributeList: set,
                         termAttributes: Query,
                         phraseAttributes: Query):
        i = 0
        while i < self.size():
            if i < self.size() - 1:
                pair = self.__terms[i].getName() + " " + self.__terms[i + 1].getName()
                if pair in attributeList:
                    phraseAttributes.__terms.append(Word(pair))
                    i = i + 2
                    continue
            if self.__terms[i].getName() in attributeList:
                termAttributes.__terms.append(self.__terms[i])
            i = i + 1
