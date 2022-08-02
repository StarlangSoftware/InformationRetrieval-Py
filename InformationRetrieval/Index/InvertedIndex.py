from collections import OrderedDict
from functools import cmp_to_key

from InformationRetrieval.Index.PostingList import PostingList
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult


class InvertedIndex:

    _index: OrderedDict = OrderedDict()

    @staticmethod
    def postingListComparator(listA: PostingList, listB: PostingList):
        if listA.size() < listB.size():
            return -1
        else:
            if listA.size() < listB.size():
                return 1
            else:
                return 0

    def __init__(self,
                 dictionaryOrfileName: object,
                 terms: [TermOccurrence] = None):
        if isinstance(dictionaryOrfileName, TermDictionary):
            dictionary: TermDictionary = dictionaryOrfileName
            if len(terms) > 0:
                term: TermOccurrence = terms[0]
                i = 1
                previousTerm = term
                termId = dictionary.getWordIndex(term.getTerm().getName())
                self.add(termId, term.getDocID())
                prevDocId = term.getDocID()
                while i < len(terms):
                    term = terms[i]
                    termId = dictionary.getWordIndex(term.getTerm().getName())
                    if termId != -1:
                        if term.isDifferent(previousTerm):
                            self.add(termId, term.getDocID())
                            prevDocId = term.getDocID()
                        else:
                            if prevDocId != term.getDocID():
                                self.add(termId, term.getDocID())
                                prevDocId = term.getDocID()
                    i = i + 1
                    previousTerm = term
        elif isinstance(dictionaryOrfileName, str):
            self.readPostingList(dictionaryOrfileName)

    def readPostingList(self, fileName: str):
        infile = open(fileName + "-postings.txt", mode="r", encoding="utf-8")
        line = infile.readline()
        while line != "":
            items = line.split(" ")
            wordId = int(items[0])
            line = infile.readline()
            self._index[wordId] = PostingList(line)
            line = infile.readline()
        infile.close()

    def save(self, fileName: str):
        outfile = open(fileName + "-postings.txt", mode="w", encoding="utf-8")
        for key in self._index.keys():
            self._index[key].writeToFile(outfile, key)
        outfile.close()

    def add(self, termId: int, docId: int):
        if termId in self._index[termId]:
            postingList = self._index[termId]
        else:
            postingList = PostingList()
        postingList.add(docId)
        self._index[termId] = postingList

    def search(self, query: Query, dictionary: TermDictionary) -> QueryResult:
        queryTerms = []
        for i in range(query.size()):
            termIndex = dictionary.getWordIndex(query.getTerm(i).getName())
            if termIndex != -1:
                queryTerms.append(self._index[termIndex])
        queryTerms.sort(key=cmp_to_key(self.postingListComparator))
        result: PostingList = queryTerms[0]
        for i in range(1, len(queryTerms)):
            result = result.intersection(queryTerms[i])
        return result.toQueryResult()