from collections import OrderedDict

from InformationRetrieval.Document.Document import Document
from InformationRetrieval.Index.PositionalPosting import PositionalPosting
from InformationRetrieval.Index.PositionalPostingList import PositionalPostingList
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult
from InformationRetrieval.Query.SearchParameter import SearchParameter
from InformationRetrieval.Query.VectorSpaceModel import VectorSpaceModel


class PositionalIndex:

    __positional_index: OrderedDict

    def constructor1(self, fileName: str):
        """
        Reads the positional inverted index from an input file.
        :param fileName: Input file name for the positional inverted index.
        """
        self.readPositionalPostingList(fileName)

    def constructor2(self, dictionary: TermDictionary, terms: list):
        """
        Constructs a positional inverted index from a list of sorted tokens. The terms array should be sorted before
        calling this method. Multiple occurrences of the same term from the same document are enlisted separately in the
        index.
        :param dictionary: Term dictionary
        :param terms: Sorted list of tokens in the memory collection.
        """
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

    def __init__(self,
                 dictionaryOrfileName: object = None,
                 terms: [TermOccurrence] = None):
        self.__positional_index = OrderedDict()
        if dictionaryOrfileName is not None:
            if isinstance(dictionaryOrfileName, TermDictionary):
                self.constructor2(dictionaryOrfileName, terms)
            elif isinstance(dictionaryOrfileName, str):
                self.constructor1(dictionaryOrfileName)

    def readPositionalPostingList(self, fileName: str):
        """
        Reads the positional postings list of the positional index from an input file. The postings are stored in n
        lines. The first line contains the term id and the number of documents that term occurs. Other n - 1 lines
        contain the postings list for that term for a separate document.
        :param fileName: Positional index file.
        """
        input_file = open(fileName + "-positionalPostings.txt", mode="r", encoding="utf-8")
        line = input_file.readline().strip()
        while line != "":
            items = line.split(" ")
            word_id = int(items[0])
            self.__positional_index[word_id] = PositionalPostingList(input_file, int(items[1]))
            line = input_file.readline().strip()
        input_file.close()

    def saveSorted(self, fileName: str):
        """
        Save positional index sorted w.r.t. index to the given output file.
        :param fileName:  Output file name.
        """
        items = []
        for key in self.__positional_index.keys():
            items.append([key, self.__positional_index[key]])
        items.sort()
        output_file = open(fileName + "-positionalPostings.txt", mode="w", encoding="utf-8")
        for item in items:
            item[1].writeToFile(output_file, item[0])
        output_file.close()

    def save(self, fileName: str):
        """
        Saves the positional index into the index file. The postings are stored in n lines. The first line contains the
        term id and the number of documents that term occurs. Other n - 1 lines contain the postings list for that term
        for a separate document.
        :param fileName: Index file name. Real index file name is created by attaching -positionalPostings.txt to this
                         file name
        """
        output_file = open(fileName + "-positionalPostings.txt", mode="w", encoding="utf-8")
        for key in self.__positional_index.keys():
            self.__positional_index[key].writeToFile(output_file, key)
        output_file.close()

    def addPosition(self,
                    termId: int,
                    docId: int,
                    position: int):
        """
        Adds a possible new term with a position and document id to the positional index. First the term is searched in
        the hash map, then the position and the document id is put into the correct postings list.
        :param termId: Id of the term
        :param docId: Document id in which the term exists
        :param position: Position of the term in the document with id docId
        """
        if termId in self.__positional_index:
            positional_posting_list = self.__positional_index[termId]
        else:
            positional_posting_list = PositionalPostingList()
        positional_posting_list.add(docId, position)
        self.__positional_index[termId] = positional_posting_list

    def positionalSearch(self,
                         query: Query,
                         dictionary: TermDictionary) -> QueryResult:
        """
        Searches a given query in the document collection using positional index boolean search.
        :param query: Query string
        :param dictionary: Term dictionary
        :return: The result of the query obtained by doing positional index boolean search in the collection.
        """
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
        """
        Returns the term frequencies  in a given document.
        :param docId: Id of the document
        :return: Term frequencies of the given document.
        """
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
        """
        Returns the document frequencies of the terms in the collection.
        :return: The document frequencies of the terms in the collection.
        """
        df = []
        i = 0
        for key in self.__positional_index.keys():
            df.append(self.__positional_index[key].size())
            i = i + 1
        return df

    def setDocumentSizes(self, documents: [Document]):
        """
        Calculates and sets the number of terms in each document in the document collection.
        :param documents: Document collection.
        """
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

    def setCategoryCounts(self, documents: [Document]):
        """
        Calculates and updates the frequency counts of the terms in each category node.
        :param documents: Document collection.
        """
        for key in self.__positional_index.keys():
            positional_posting_list = self.__positional_index[key]
            for i in range(positional_posting_list.size()):
                positional_posting = positional_posting_list.get(i)
                doc_id = positional_posting.getDocId()
                documents[doc_id].getCategoryNode().addCounts(key, positional_posting.size())

    def rankedSearch(self,
                     query: Query,
                     dictionary: TermDictionary,
                     documents: [Document],
                     parameter: SearchParameter) -> QueryResult:
        """
        Searches a given query in the document collection using inverted index ranked search.
        :param query: Query string
        :param dictionary: Term dictionary
        :param documents: Document collection.
        :param parameter: Search parameter.
        :return: The result of the query obtained by doing inverted index ranked search in the collection.
        """
        N = len(documents)
        result = QueryResult()
        scores = {}
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
                        score = VectorSpaceModel.weighting(tf,
                                                           df,
                                                           N,
                                                           parameter.getTermWeighting(),
                                                           parameter.getDocumentWeighting())
                        if doc_id in scores:
                            scores[doc_id] = scores[doc_id] + score
                        else:
                            scores[doc_id] = score
        for doc_id in scores:
            result.add(doc_id, scores[doc_id])
        return result
