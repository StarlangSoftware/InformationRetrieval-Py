from collections import OrderedDict
from functools import cmp_to_key

from InformationRetrieval.Index.PostingList import PostingList
from InformationRetrieval.Index.TermDictionary import TermDictionary
from InformationRetrieval.Index.TermOccurrence import TermOccurrence
from InformationRetrieval.Query.Query import Query
from InformationRetrieval.Query.QueryResult import QueryResult


class InvertedIndex:

    __index: OrderedDict

    def constructor1(self, fileName: str):
        """
        Reads the inverted index from an input file.
        :param fileName: Input file name for the inverted index.
        """
        self.readPostingList(fileName)

    def constructor2(self, dictionary: TermDictionary, terms: list):
        """
        Constructs an inverted index from a list of sorted tokens. The terms array should be sorted before calling this
        method. Multiple occurrences of the same term from the same document are merged in the index. Instances of the
        same term are then grouped, and the result is split into a postings list.
        :param dictionary: Term dictionary
        :param terms: Sorted list of tokens in the memory collection.
        """
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

    def __init__(self,
                 dictionaryOrfileName: object = None,
                 terms: [TermOccurrence] = None):
        self.__index = OrderedDict()
        if dictionaryOrfileName is not None:
            if isinstance(dictionaryOrfileName, TermDictionary):
                self.constructor2(dictionaryOrfileName, terms)
            elif isinstance(dictionaryOrfileName, str):
                self.constructor1(dictionaryOrfileName)

    def readPostingList(self, fileName: str):
        """
        Reads the postings list of the inverted index from an input file. The postings are stored in two lines. The first
        line contains the term id and the number of postings for that term. The second line contains the postings
        list for that term.
        :param fileName: Inverted index file.
        """
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
        """
        Save inverted index sorted w.r.t. index to the given output file.
        :param fileName:  Output file name.
        """
        items = []
        for key in self.__index.keys():
            items.append([key, self.__index[key]])
        items.sort()
        output_file = open(fileName + "-postings.txt", mode="w", encoding="utf-8")
        for item in items:
            item[1].writeToFile(output_file, item[0])
        output_file.close()

    def save(self, fileName: str):
        """
        Saves the inverted index into the index file. The postings are stored in two lines. The first
        line contains the term id and the number of postings for that term. The second line contains the postings
        list for that term.
        :param fileName: Index file name. Real index file name is created by attaching -postings.txt to this
                         file name
        """
        output_file = open(fileName + "-postings.txt", mode="w", encoding="utf-8")
        for key in self.__index.keys():
            self.__index[key].writeToFile(output_file, key)
        output_file.close()

    def add(self,
            termId: int,
            docId: int):
        """
        Adds a possible new term with a document id to the inverted index. First the term is searched in the hash map,
        then the document id is put into the correct postings list.
        :param termId: Id of the term
        :param docId: Document id in which the term exists
        """
        if termId in self.__index:
            posting_list = self.__index[termId]
        else:
            posting_list = PostingList()
        posting_list.add(docId)
        self.__index[termId] = posting_list

    def autoCompleteWord(self,
                         wordList: [str],
                         dictionary: TermDictionary):
        """
        Constructs a sorted array list of frequency counts for a word list and also sorts the word list according to
        those frequencies.
        :param wordList: Word list for which frequency array is constructed.
        :param dictionary: Term dictionary
        """
        counts = []
        for word in wordList:
            counts.append(self.__index[dictionary.getWordIndex(word)].size())
        for i in range(len(wordList) - 1):
            for j in range(i + 1, len(wordList)):
                if counts[i] < counts[j]:
                    counts[i], counts[j] = counts[j], counts[i]
                    wordList[i], wordList[j] = wordList[j], wordList[i]

    def search(self,
               query: Query,
               dictionary: TermDictionary) -> QueryResult:
        """
        Searches a given query in the document collection using inverted index boolean search.
        :param query: Query string
        :param dictionary: Term dictionary
        :return: The result of the query obtained by doing inverted index boolean search in the collection.
        """
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
