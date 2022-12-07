from __future__ import annotations

from DataStructure.CounterHashMap import CounterHashMap

from InformationRetrieval.Index.Term import Term
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Query.Query import Query


class CategoryNode:

    __children: [CategoryNode]
    __parent: CategoryNode
    __counts: CounterHashMap
    __category_words: [str]

    def __init__(self, name: str, parent: CategoryNode):
        self.__category_words = name.split()
        self.__parent = parent
        self.__counts = CounterHashMap()
        self.__children = []
        if parent is not None:
            parent.addChild(self)

    def addChild(self, child: CategoryNode):
        self.__children.append(child)

    def getName(self) -> str:
        result = self.__category_words[0]
        for i in range(1, len(self.__category_words)):
            result += " " + self.__category_words[i]
        return result

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

    def isDescendant(self, ancestor: CategoryNode) -> bool:
        if self == ancestor:
            return True
        if self.__parent is None:
            return False
        return self.__parent.isDescendant(ancestor)

    def getChildren(self) -> [CategoryNode]:
        return self.__children

    def __str__(self) -> str:
        if self.__parent is not None:
            if self.__parent.__parent is not None:
                return self.__parent.__str__() + "%" + self.getName()
            else:
                return self.getName()
        return ""

    def setRepresentativeCount(self, representativeCount: int):
        if representativeCount <= len(self.__counts):
            top_list = self.__counts.topN(representativeCount)
            self.__counts = CounterHashMap()
            for item in top_list:
                self.__counts.putNTimes(item[0], item[1])

    def getCategoriesWithKeyword(self,
                                 query: Query,
                                 result: list):
        category_score = 0
        for i in range(query.size()):
            if query.getTerm(i).getName() in self.__category_words:
                category_score = category_score + 1
        if category_score > 0:
            result.append(self)
        for child in self.__children:
            child.getCategoriesWithKeyword(query, result)

    def getCategoriesWithCosine(self,
                                query: Query,
                                dictionary: TermDictionary,
                                result: list):
        category_score = 0
        for i in range(query.size()):
            term = dictionary.getWord(query.getTerm(i).getName())
            if term is not None and isinstance(term, Term):
                category_score = category_score + self.__counts.count(term.getTermId())
        if category_score > 0:
            result.append(self)
        for child in self.__children:
            child.getCategoriesWithCosine(query, dictionary, result)

    def __repr__(self):
        return self.getName() + "(" + self.__children.__repr__() + ")"
