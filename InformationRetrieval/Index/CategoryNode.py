from __future__ import annotations

from DataStructure.CounterHashMap import CounterHashMap
from Dictionary.Word import Word

from InformationRetrieval.Index.TermDictionary import TermDictionary


class CategoryNode:

    __name: str
    __children: [CategoryNode]
    __parent: CategoryNode
    __counts: CounterHashMap

    def __init__(self, name: str, parent: CategoryNode):
        self.__name = name
        self.__parent = parent
        self.__counts = CounterHashMap()
        self.__children = []
        if parent is not None:
            parent.addChild(self)

    def addChild(self, child: CategoryNode):
        self.__children.append(child)

    def getName(self):
        return self.__name

    def getChild(self, childName: str) -> CategoryNode:
        for child in self.__children:
            if child.getName() == childName:
                return child
        return None

    def addCounts(self, termId: int, count: int):
        current = self
        while current.__parent is not None:
            current.__counts.putNTimes(termId, count)
            current = current.__parent

    def getChildren(self) -> [CategoryNode]:
        return self.__children

    def topN(self, N: int) -> list:
        if N <= len(self.__counts):
            return self.__counts.topN(N)
        else:
            return self.__counts.topN(len(self.__counts))

    def topNString(self, dictionary: TermDictionary, N: int) -> str:
        top_n = self.topN(N)
        result = self.__str__()
        for item in top_n:
            if not Word.isPunctuationSymbol(dictionary.getWordWithIndex(item[1]).getName()):
                result = result + "\t" + dictionary.getWordWithIndex(item[1]).getName() + " (" + item[0].__str__() + ")"
        return result

    def __str__(self) -> str:
        if self.__parent is not None:
            if self.__parent.__parent is not None:
                return self.__parent.__str__() + "%" + self.__name
            else:
                return self.__name
        return ""

    def __repr__(self):
        return self.__name + "(" + self.__children.__repr__() + ")"
