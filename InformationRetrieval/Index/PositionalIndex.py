from collections import OrderedDict

from InformationRetrieval.Document.Document import Document
from InformationRetrieval.Document.DocumentWeighting import DocumentWeighting
from InformationRetrieval.Index.PositionalPosting import PositionalPosting
from InformationRetrieval.Index.PositionalPostingList import PositionalPostingList
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Index.TermWeighting import TermWeighting
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult
from InformationRetrieval.Query.VectorSpaceModel import VectorSpaceModel


class PositionalIndex:

    __positional_index: OrderedDict

    def __init__(self,
                 dictionaryOrfileName: object = None,
                 terms: [TermOccurrence] = None):
        self.__positional_index = OrderedDict()
        if dictionaryOrfileName is not None:
            if isinstance(dictionaryOrfileName, TermDictionary):
                dictionary: TermDictionary = dictionaryOrfileName
                if len(terms) > 0:
                    term: TermOccurrence = terms[0]
                    i = 1
                    previous_term = term
                    term_id = dictionary.getWordIndex(term.getTerm().getName())
                    self.addPosition(term_id, term.getDocId(), term.getPosition())
                    prev_doc_id = term.getDocId()
                    while i < len(terms):
                        term = terms[i]
                        term_id = dictionary.getWordIndex(term.getTerm().getName())
                        if term_id != -1:
                            if term.isDifferent(previous_term):
                                self.addPosition(term_id, term.getDocId(), term.getPosition())
                                prev_doc_id = term.getDocId()
                            elif prev_doc_id != term.getDocId():
                                self.addPosition(term_id, term.getDocId(), term.getPosition())
                                prev_doc_id = term.getDocId()
                            else:
                                self.addPosition(term_id, term.getDocId(), term.getPosition())
                        i = i + 1
                        previous_term = term
            elif isinstance(dictionaryOrfileName, str):
                self.readPositionalPostingList(dictionaryOrfileName)

    def readPositionalPostingList(self, fileName: str):
        input_file = open(fileName + "-positionalPostings.txt", mode="r", encoding="utf-8")
        line = input_file.readline().strip()
        while line != "":
            items = line.split(" ")
            word_id = int(items[0])
            self.__positional_index[word_id] = PositionalPostingList(input_file, int(items[1]))
            line = input_file.readline().strip()
        input_file.close()

    def saveSorted(self, fileName: str):
        items = []
        for key in self.__positional_index.keys():
            items.append([key, self.__positional_index[key]])
        items.sort()
        output_file = open(fileName + "-positionalPostings.txt", mode="w", encoding="utf-8")
        for item in items:
            item[1].writeToFile(output_file, item[0])
        output_file.close()

    def save(self, fileName: str):
        output_file = open(fileName + "-positionalPostings.txt", mode="w", encoding="utf-8")
        for key in self.__positional_index.keys():
            self.__positional_index[key].writeToFile(output_file, key)
        output_file.close()

    def addPosition(self,
                    termId: int,
                    docId: int,
                    position: int):
        if termId in self.__positional_index:
            positional_posting_list = self.__positional_index[termId]
        else:
            positional_posting_list = PositionalPostingList()
        positional_posting_list.add(docId, position)
        self.__positional_index[termId] = positional_posting_list

    def positionalSearch(self,
                         query: Query,
                         dictionary: TermDictionary) -> QueryResult:
        posting_result: PositionalPostingList = None
        for i in range(query.size()):
            term = dictionary.getWordIndex(query.getTerm(i).getName())
            if term != -1:
                if i == 0:
                    posting_result = self.__positional_index[term]
                elif posting_result is not None:
                    posting_result = posting_result.intersection(self.__positional_index[term])
                else:
                    return QueryResult()
            else:
                return QueryResult()
        if posting_result is not None:
            return posting_result.toQueryResult()
        else:
            return QueryResult()

    def getTermFrequencies(self, docId: int) -> [int]:
        tf = []
        i = 0
        for key in self.__positional_index.keys():
            positional_posting_list = self.__positional_index[key]
            index = positional_posting_list.getIndex(docId)
            if index != -1:
                tf.append(positional_posting_list.get(index).size())
            else:
                tf.append(0)
            i = i + 1
        return tf

    def getDocumentFrequencies(self) -> [int]:
        df = []
        i = 0
        for key in self.__positional_index.keys():
            df.append(self.__positional_index[key].size())
            i = i + 1
        return df

    def setDocumentSizes(self, documents: [Document]):
        sizes = []
        for i in range(len(documents)):
            sizes.append(0)
        for key in self.__positional_index.keys():
            positional_posting_list = self.__positional_index[key]
            for i in range(positional_posting_list.size()):
                positional_posting = positional_posting_list.get(i)
                doc_id = positional_posting.getDocId()
                sizes[doc_id] = sizes[doc_id] + positional_posting.size()
        for doc in documents:
            doc.setSize(sizes[doc.getDocId()])

    def rankedSearch(self,
                     query: Query,
                     dictionary: TermDictionary,
                     documents: [Document],
                     termWeighting: TermWeighting,
                     documentWeighting: DocumentWeighting) -> QueryResult:
        N = len(documents)
        result = QueryResult()
        scores = [0 for _ in range(N)]
        for i in range(query.size()):
            term = dictionary.getWordIndex(query.getTerm(i).getName())
            if term != -1:
                positional_posting_list = self.__positional_index[term]
                for j in range(positional_posting_list.size()):
                    positional_posting: PositionalPosting = positional_posting_list.get(j)
                    doc_id = positional_posting.getDocId()
                    tf = positional_posting.size()
                    df = self.__positional_index[term].size()
                    if tf > 0 and df > 0:
                        scores[doc_id] = scores[doc_id] + VectorSpaceModel.weighting(tf, df, N, termWeighting, documentWeighting)
        for i in range(N):
            scores[i] = scores[i] / documents[i].getSize()
            if scores[i] > 0:
                result.add(i, scores[i])
        result.sort()
        return result
