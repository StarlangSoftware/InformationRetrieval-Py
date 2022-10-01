from __future__ import annotations
from typing import TextIO

from InformationRetrieval.Index.PositionalPosting import PositionalPosting
from InformationRetrieval.Index.Posting import Posting
from InformationRetrieval.Query.QueryResult import QueryResult


class PositionalPostingList:

    __postings: [PositionalPosting]

    def __init__(self,
                 infile: TextIO = None,
                 count: int = None):
        self.__postings = []
        if infile is not None:
            for i in range(count):
                line = infile.readline().strip()
                ids = line.split(" ")
                number_of_positional_postings = int(ids[1])
                if len(ids) == number_of_positional_postings + 2:
                    doc_id = int(ids[0])
                    for j in range(number_of_positional_postings):
                        positional_posting = int(ids[j + 2])
                        self.add(doc_id, positional_posting)

    def size(self) -> int:
        return len(self.__postings)

    def getIndex(self, docId: int) -> int:
        begin = 0
        end = self.size() - 1
        while begin <= end:
            middle = (begin + end) // 2
            if docId == self.__postings[middle].getDocId():
                return middle
            else:
                if docId == self.__postings[middle].getDocId():
                    end = middle - 1
                else:
                    begin = middle + 1
        return -1

    def toQueryResult(self) -> QueryResult:
        result = QueryResult()
        for posting in self.__postings:
            result.add(posting.getDocId())
        return result

    def add(self,
            docId: int,
            position: int):
        index = self.getIndex(docId)
        if index == -1:
            self.__postings.append(PositionalPosting(docId))
            self.__postings[len(self.__postings) - 1].add(position)
        else:
            self.__postings[index].add(position)

    def get(self, index: int) -> PositionalPosting:
        return self.__postings[index]

    def union(self, secondList: PositionalPostingList) -> PositionalPostingList:
        result = PositionalPostingList()
        result.__postings.extend(self.__postings)
        result.__postings.extend(secondList.__postings)
        return result

    def intersection(self, secondList: PositionalPostingList) -> PositionalPostingList:
        i = 0
        j = 0
        result = PositionalPostingList()
        while i < len(self.__postings) and j < len(secondList.__postings):
            p1: PositionalPosting = self.__postings[i]
            p2: PositionalPosting = secondList.__postings[j]
            if p1.getDocId() == p2.getDocId():
                position1 = 0
                position2 = 0
                postings1 = p1.getPositions()
                postings2 = p2.getPositions()
                while position1 < len(postings1) and position2 < len(postings2):
                    posting1: Posting = postings1[position1]
                    posting2: Posting = postings2[position2]
                    if posting1.getId() + 1 == posting2.getId():
                        result.add(p1.getDocId(), posting2.getId())
                        position1 = position1 + 1
                        position2 = position2 + 1
                    else:
                        if posting1.getId() + 1 < posting2.getId():
                            position1 = position1 + 1
                        else:
                            position2 = position2 + 1
                i = i + 1
                j = j + 1
            else:
                if p1.getDocId() < p2.getDocId():
                    i = i + 1
                else:
                    j = j + 1
        return result

    def __str__(self) -> str:
        result = ""
        for positional_posting in self.__postings:
            result = result + "\t" + positional_posting.__str__() + "\n"
        return result

    def writeToFile(self,
                    outfile: TextIO,
                    index: int):
        if self.size() > 0:
            outfile.write(index.__str__() + " " + self.size().__str__() + "\n")
            outfile.write(self.__str__())
