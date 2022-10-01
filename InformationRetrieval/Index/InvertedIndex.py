from collections import OrderedDict
from functools import cmp_to_key

from InformationRetrieval.Index.PostingList import PostingList
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult


class InvertedIndex:

    __index: OrderedDict

    def __init__(self,
                 dictionaryOrfileName: object = None,
                 terms: [TermOccurrence] = None):
        self.__index = OrderedDict()
        if dictionaryOrfileName is not None:
            if isinstance(dictionaryOrfileName, TermDictionary):
                dictionary: TermDictionary = dictionaryOrfileName
                if len(terms) > 0:
                    term: TermOccurrence = terms[0]
                    i = 1
                    previous_term = term
                    term_id = dictionary.getWordIndex(term.getTerm().getName())
                    self.add(term_id, term.getDocId())
                    prev_doc_id = term.getDocId()
                    while i < len(terms):
                        term = terms[i]
                        term_id = dictionary.getWordIndex(term.getTerm().getName())
                        if term_id != -1:
                            if term.isDifferent(previous_term):
                                self.add(term_id, term.getDocId())
                                prev_doc_id = term.getDocId()
                            else:
                                if prev_doc_id != term.getDocId():
                                    self.add(term_id, term.getDocId())
                                    prev_doc_id = term.getDocId()
                        i = i + 1
                        previous_term = term
            elif isinstance(dictionaryOrfileName, str):
                self.readPostingList(dictionaryOrfileName)

    def readPostingList(self, fileName: str):
        input_file = open(fileName + "-postings.txt", mode="r", encoding="utf-8")
        line = input_file.readline().strip()
        while line != "":
            items = line.split(" ")
            word_id = int(items[0])
            line = input_file.readline().strip()
            self.__index[word_id] = PostingList(line)
            line = input_file.readline()
        input_file.close()

    def saveSorted(self, fileName: str):
        items = []
        for key in self.__index.keys():
            items.append([key, self.__index[key]])
        items.sort()
        output_file = open(fileName + "-postings.txt", mode="w", encoding="utf-8")
        for item in items:
            item[1].writeToFile(output_file, item[0])
        output_file.close()

    def save(self, fileName: str):
        output_file = open(fileName + "-postings.txt", mode="w", encoding="utf-8")
        for key in self.__index.keys():
            self.__index[key].writeToFile(output_file, key)
        output_file.close()

    def add(self,
            termId: int,
            docId: int):
        if termId in self.__index:
            posting_list = self.__index[termId]
        else:
            posting_list = PostingList()
        posting_list.add(docId)
        self.__index[termId] = posting_list

    def search(self,
               query: Query,
               dictionary: TermDictionary) -> QueryResult:
        query_terms = []
        for i in range(query.size()):
            term_index = dictionary.getWordIndex(query.getTerm(i).getName())
            if term_index != -1:
                query_terms.append(self.__index[term_index])
            else:
                return QueryResult()
        query_terms.sort(key=cmp_to_key(PostingList.postingListComparator))
        result: PostingList = query_terms[0]
        for i in range(1, len(query_terms)):
            result = result.intersection(query_terms[i])
        return result.toQueryResult()
