from __future__ import annotations

from io import TextIOWrapper

from InformationRetrieval.Index.Posting import Posting
from InformationRetrieval.Query.QueryResult import QueryResult


class PostingList:

    postings: [Posting] = []

    def __init__(self, line: str = None):
        if line is not None:
            ids = line.split(" ")
            for id in ids:
                self.add(int(id))

    def add(self, docId: int):
        self.postings.append(Posting(docId))

    def size(self) -> int:
        return len(self.postings)

    def intersection(self, secondList: PostingList) -> PostingList:
        i = 0
        j = 0
        result = PostingList()
        while i < self.size() and j < secondList.size():
            p1 : Posting = self.postings[i]
            p2 : Posting = secondList.postings[j]
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
        result.postings.append(self.postings)
        result.postings.append(secondList.postings)
        return result

    def toQueryResult(self) -> QueryResult:
        result = QueryResult()
        for posting in self.postings:
            result.add(posting.getId())
        return result

    def writeToFile(self, outfile: TextIOWrapper, index: int):
        if self.size() > 0:
            outfile.write(index.__str__() + " " + self.size().__str__() + "\n")
            outfile.write(self.__str__())

    def __str__(self):
        result = ""
        for posting in self.postings:
            result = result + posting.getId()
        return result.strip() + "\n"
