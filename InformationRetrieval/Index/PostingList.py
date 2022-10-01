from __future__ import annotations

from typing import TextIO

from InformationRetrieval.Index.Posting import Posting
from InformationRetrieval.Query.QueryResult import QueryResult


class PostingList:

    __postings: [Posting]

    @staticmethod
    def postingListComparator(listA: PostingList,
                              listB: PostingList):
        if listA.size() < listB.size():
            return -1
        else:
            if listA.size() < listB.size():
                return 1
            else:
                return 0

    def __init__(self, line: str = None):
        self.__postings = []
        if line is not None:
            ids = line.split(" ")
            for _id in ids:
                self.add(int(_id))

    def add(self, docId: int):
        self.__postings.append(Posting(docId))

    def size(self) -> int:
        return len(self.__postings)

    def intersection(self, secondList: PostingList) -> PostingList:
        i = 0
        j = 0
        result = PostingList()
        while i < self.size() and j < secondList.size():
            p1: Posting = self.__postings[i]
            p2: Posting = secondList.__postings[j]
            if p1.getId() == p2.getId():
                result.add(p1.getId())
                i = i + 1
                j = j + 1
            else:
                if p1.getId() < p2.getId():
                    i = i + 1
                else:
                    j = j + 1
        return result

    def union(self, secondList: PostingList) -> PostingList:
        result = PostingList()
        result.__postings.extend(self.__postings)
        result.__postings.extend(secondList.__postings)
        return result

    def toQueryResult(self) -> QueryResult:
        result = QueryResult()
        for posting in self.__postings:
            result.add(posting.getId())
        return result

    def writeToFile(self, outfile: TextIO, index: int):
        if self.size() > 0:
            outfile.write(index.__str__() + " " + self.size().__str__() + "\n")
            outfile.write(self.__str__())

    def __str__(self):
        result = ""
        for posting in self.__postings:
            result = result + posting.getId().__str__() + " "
        return result.strip() + "\n"
