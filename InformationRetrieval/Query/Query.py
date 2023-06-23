from __future__ import annotations

import re

from Dictionary.Word import Word


class Query:

    __terms: [Word]
    __shortcuts: list = ["cc", "cm2", "cm", "gb", "ghz", "gr", "gram", "hz", "inc", "inch", "inç", "kg", "kw", "kva",
                         "litre", "lt", "m2", "m3", "mah", "mb", "metre", "mg", "mhz", "ml", "mm", "mp", "ms",
                         "mt", "mv", "tb", "tl", "va", "volt", "watt", "ah", "hp", "oz", "rpm", "dpi", "ppm", "ohm",
                         "kwh", "kcal", "kbit", "mbit", "gbit", "bit", "byte", "mbps", "gbps", "cm3", "mm2", "mm3",
                         "khz", "ft", "db", "sn", "g", "v", "m", "l", "w", "s"]

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
                         phraseAttributes: Query) -> Query:
        i = 0
        filtered_query = Query()
        while i < self.size():
            if i < self.size() - 1:
                pair = self.__terms[i].getName() + " " + self.__terms[i + 1].getName()
                if pair in attributeList:
                    phraseAttributes.__terms.append(Word(pair))
                    i = i + 2
                    continue
                if self.__terms[i + 1].getName() in self.__shortcuts and re.fullmatch("[+-]?\\d+|[+-]?(\\d+)?\\.\\d*",
                                                                                      self.__terms[i].getName()):
                    phraseAttributes.__terms.append(Word(pair))
                    i = i + 2
                    continue
            if self.__terms[i].getName() in attributeList:
                termAttributes.__terms.append(self.__terms[i])
            else:
                filtered_query.__terms.append(self.__terms[i])
            i = i + 1
        return filtered_query
